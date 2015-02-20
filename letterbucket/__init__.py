import flask

from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

default_view = flask.Blueprint('letterbucket', __name__,
                               template_folder='templates',  static_folder='static',
                               static_url_path='', url_prefix='')
from letterbucket.account import view as account_view


def create_application(config_file=None, config_object=None):
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
        flask.g.db_handle = db
    app.register_blueprint(default_view)
    print default_view.url_prefix, default_view.static_url_path
    app.register_blueprint(account_view)
    return app


@default_view.route('/')
def index_page():
    return flask.render_template('index.html')
