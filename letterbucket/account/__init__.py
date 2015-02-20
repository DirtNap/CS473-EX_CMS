import flask

import users

view = flask.Blueprint('account', __name__, template_folder='templates')

@view.route('/login')
def login_page():
    return flask.render_template('login.html')

@view.route('/login', methods=['POST'])
def process_login():
    username = flask.request.form['username']
    raw_password = flask.request.form['password']
    (errors, user) = ("", None)
    if not all((username, raw_password)):
        errors = "Missing Values"
    else:
        user = users.User.GetByUsername(username)
        if user:
            if not user.validate_password(raw_password):
                errors = "Incorrect password"
        else:
            errors = "User %s not found" % (username,)
    if errors:
        flask.flash(errors, 'error')
        return flask.redirect(flask.url_for('.login_page'))
    flask.flash('Login Succeeded')
    return flask.render_template('login_result.html', username=username)

