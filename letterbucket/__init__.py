import flask

from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

# Singleton database handle
db = SQLAlchemy()
# Singleton login manager
login_manager = LoginManager()

# Create or import views needed by the app
default_view = flask.Blueprint('letterbucket', __name__,
                               template_folder='templates',  static_folder='static',
                               static_url_path='', url_prefix='')
from letterbucket.account import view as account_view
from letterbucket.content import view as content_view
from letterbucket.content import posts, blogs
from letterbucket.utilities.filters import Filters

def create_application(config_file=None, config_object=None):
    """Factory for creating applications

    Arguments:
      config_file: a file representation of a dict
      config_object: an object with constant members for config

    Returns:  a flask.Flask application with 

    """
    app = flask.Flask(__name__)
    if all((config_file, config_object)):
        raise ValueError("Too many config types provided")
    if not any((config_file, config_object)):
        raise ValueError("No config type provided for application.")
    if config_file:
        app.config.from_pyfile(config_file)
    else:
        app.config.from_object(config_object)
    db.init_app(app)
    login_manager.init_app(app)
    for attr in dir(Filters):
        if not attr.startswith('_'):
            app.jinja_env.filters[attr] = getattr(Filters, attr)
    with app.app_context():
        # put the database handle in the global session
        flask.g.db_handle = db
    # Register the required views
    app.register_blueprint(default_view)
    app.register_blueprint(account_view)
    app.register_blueprint(content_view)
    return app


@default_view.route('/', defaults={'path': None, 'post': 0})
@default_view.route('/<path>', defaults={'post': 0})
@default_view.route('/<path>/<int:post>')
def index_page(path, post):
    print 'path: %s, post: %d' % (path, post)
    published = posts.PostStatus('Published')
    query = posts.Post.query.filter_by(status_id=published.id)
    if path:
        target_blog = blogs.Blog.GetByPath(path)
        if not target_blog:
            flask.abort(404)
        query = query.filter_by(blog_id=target_blog.id)
    if post > 0:
        query = query.filter_by(id=post)
    all_posts = query.order_by(posts.Post.pub_date.desc()).limit(100).all()
    if not all_posts:
        flask.abort(404)
    should_truncate = (post == 0)
    print should_truncate
    return flask.render_template('index.html',
                                 posts=all_posts,
                                 truncate=should_truncate)
@default_view.route('/edit_post')
def edit_post():
  return flask.render_template('edit_post.html')

@default_view.route('/view_all')
def view_all():
  return flask.render_template('view_all.html')
