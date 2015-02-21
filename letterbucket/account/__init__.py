import flask
from flask.ext import login

import users
from .. import login_manager
from ..content import blogs

view = flask.Blueprint('account', __name__, template_folder='templates')
login_manager.login_view = '.login_page'
login_manager.refresh_view = '.login_page'

@view.route('/login')
def login_page():
    """Display the login form."""
    return flask.render_template('login.html')

@view.route('/login', methods=['POST'])
def process_login():
    """Process the login form."""
    username = flask.request.form['username']
    raw_password = flask.request.form['password']
    (errors, user) = ('', None)
    # Make sure username and password are 
    if not all((username, raw_password)):
        errors = 'Missing Values'
    else:
        # Make sure the user logging in exists
        user = users.User.GetByUsername(username)
        if user:
            # Make sure the passwords match
            if not user.ValidatePassword(raw_password):
                errors = 'Incorrect password'
        else:
            errors = 'User %s not found' % (username,)
    if errors:
        flask.flash(errors, 'error')
        return flask.redirect(flask.url_for('.login_page'))
    # log the user in via the login system
    if login.login_user(user, remember=bool(flask.request.form.get('remember'))):
        flask.flash('Login Succeeded')
    else:
        flask.flash('Login Error', 'error')
    return flask.redirect(flask.request.args.get('next') or flask.url_for('.user_profile'))


@view.route('/logout', methods=['GET', 'POST'])
def process_logout():
    """Utility page to logout the user."""
    login.logout_user()
    return flask.redirect(flask.request.args.get('next') or flask.url_for('.login_page'))


@view.route('/profile', methods=['GET'])
@login.login_required
def user_profile():
    """Displays the user's profile information."""
    return flask.render_template('profile.html', reset_link=flask.url_for('.pw_reset_page'))


@view.route('/create')
def create_user_page():
    """Displays the create user form."""
    # Existing users should not create
    # TODO(dirtnap): Update this when account management is implemented
    if login.current_user.is_authenticated():
        return flask.redirect(flask.url_for('.user_profile'))
    return flask.render_template('create.html')

@view.route('/create', methods=['POST'])
def process_create_user():
    """Create new users."""
    ok_to_create = True
    form_keys = ('username', 'email', 'name', 'password', 'blog_path', 'blog_name')
    # Make sure all form fields are filled out
    for k in form_keys:
        if not flask.request.form.get(k):
            flask.flash('Missing field:  %s' % (k,), 'error')
            ok_to_create = False
    # Make sure the username is available
    if flask.request.form['username']:
        new_user = users.User.GetByUsername(flask.request.form['username'])
        if new_user:
            flask.flash('Username %s is not available.' % (flask.request.form['username'],), 'error')
            new_user = None
            ok_to_create = False
    # Make sure the email is not in use
    if flask.request.form['email']:
        new_user = users.User.GetByEmail(flask.request.form['email'])
        if new_user:
            flask.flash('E-mail address %s is already in use.' % (flask.request.form['email'],), 'error')
            new_user = None
            ok_to_create = False
    # Make sure the path is not in use
    if flask.request.form['blog_path']:
        new_blog = blogs.Blog.GetByPath(flask.request.form['blog_path'])
        if new_blog:
            flask.flash('Blog path %s is not available' % (flask.request.form['blog_path'],), 'error')
            new_blog = None
            ok_to_create = False
    if ok_to_create:
        # First create and persist the user.
        new_user = users.User(flask.request.form['username'],
                              flask.request.form['email'],
                              flask.request.form['name'],
                              flask.request.form['password'])
        new_user.Persist()
        # Now create and persist the blog.
        new_blog = blogs.Blog(flask.request.form['blog_path'],
                              flask.request.form['blog_name'],
                              new_user)
        new_blog.Persist()
        flask.flash('Account Created.  Please Log In')
        return flask.redirect(flask.url_for('.login_page'))
    else:
        # Something failed.  Let the user try again.
        return flask.redirect(flask.url_for('.create_user_page'))

@view.route('/reset')
@login.fresh_login_required
def pw_reset_page():
    """Display the password reset form."""
    return flask.render_template('pw_reset.html')

@view.route('/reset', methods=['POST'])
@login.fresh_login_required
def process_pw_reset():
    """Process a password change request."""
    ok_to_change = True
    # Make sure the form is filled out
    if not all((flask.request.form.get('old_password'),
                flask.request.form.get('new_password'),
                flask.request.form.get('repeat_password'))):
        flask.flash('Missing fields', 'error')
        ok_to_change = False
    # Make sure the new password is confirmed
    if flask.request.form.get('new_password') != flask.request.form.get('repeat_password'):
        flask.flash('Passwords do not match', 'error')
        ok_to_change = False
    # Make sure the old password is correct.
    if not login.current_user.ValidatePassword(flask.request.form.get('old_password')):
        flask.flash('Invalid Password', 'error')
        ok_to_change = False
    if ok_to_change:
        login.current_user.SetPassword(flask.request.form['new_password'])
        login.current_user.Persist()
        return flask.redirect(flask.url_for('.user_profile'))
    else:
        return flask.redirect(flask.url_for('.pw_reset_page'))
        
        
