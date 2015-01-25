import flask
import md5
import sqlite3

DEBUG = True
SECRET_KEY = 'Team 2 Rules'

def GetDatabaseConnection(path=':memory:'):
    """Get a database connection, and initialize the db if necessary."""
    db_connection = sqlite3.connect(path)  # Connect to a local sql database
    db_connection.text_factory = str  # We don't need to deal with unicode here.
    _SetUpDatabase(db_connection)
    return db_connection

def _SetUpDatabase(con):
    cur = con.cursor()  # Get a database cursor
    try:
        # See if there's a users table
        cur.execute('SELECT * FROM users')
        # There is.  We're all set up, so return.
        return
    except sqlite3.OperationalError:
        # There wasn't.  Keep going in this function.
        pass
    # Create a table, and insert the default value
    cur.execute('CREATE TABLE users(login_name TEXT PRIMARY KEY, password_hash TEXT NOT NULL, content_path TEXT UNIQUE)')
    cur.execute('INSERT INTO users VALUES (?, ?, ?)', ('admin', md5.new('admin_password').hexdigest(), 'site_news'))
    con.commit()

# This module is a flask app
app = flask.Flask(__name__)
# Read the config from all the all-caps variables in this module
app.config.from_object(__name__)

# These @ things are called decorators.  They make a function do something extra, like handle a route or a control phase
@app.before_request
def before_request():
    flask.g.db_conn = GetDatabaseConnection()

@app.teardown_request
def teardown_request(exception):
    con = getattr(flask.g, 'db_conn', None)
    if con:
        con.close()

@app.route('/', methods=['GET'])
def login_page():
    return flask.render_template('login.html')

@app.route('/login', methods=['POST'])
def process_login():
    username = flask.request.form['username']
    raw_password = flask.request.form['password']
    (errors, path) = ("", "")
    if not all((username, raw_password)):
        errors = "Missing Values"
    else:
        pw_hash = md5.new(raw_password)
        cursor = flask.g.db_conn.cursor()
        cursor.execute('SELECT password_hash, content_path FROM users WHERE login_name=?', (username,))
        row = cursor.fetchone()
        if not row:
            errors = "Unknwon User %s" % (username,)
        else:
            chk_pw, path = row
            if chk_pw != pw_hash.hexdigest():
                errors = "Wrong Password"
    if errors:
        flask.flash(errors)
        return flask.redirect(flask.url_for('login_page'))
    return flask.render_template('login_result.html', path=path, username=username)

if __name__ == '__main__':
    con = GetDatabaseConnection()
    app.run()
    con.close()
