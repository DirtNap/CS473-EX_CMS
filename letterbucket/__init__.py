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
from letterbucket.content import posts

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
    with app.app_context():
        # put the database handle in the global session
        flask.g.db_handle = db
    # Register the required views
    app.register_blueprint(default_view)
    app.register_blueprint(account_view)
    app.register_blueprint(content_view)
    return app


@default_view.route('/')
def index_page():
    """Default template.  This is only a placeholder."""
    # TODO(???): replace this with an aggregate default view from the content module.
    published = posts.PostStatus('Published')
    all_posts = posts.Post.query.filter_by(
        status_id=published.id).order_by(posts.Post.create_date, posts.Post.blog_id)
    return flask.render_template('index.html', posts=all_posts)
