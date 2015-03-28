import flask
from flask.ext import login

import users
import forms
from .. import login_manager
from ..content import blogs

view = flask.Blueprint('account', __name__, template_folder='templates')
login_manager.login_view = 'account.login_page'
login_manager.refresh_view = 'account.login_page'

@view.route('/login', methods=['GET', 'POST'])
def login_page():
    """Process the login form."""
    (errors, user) = ('', None)
    form = forms.LoginForm()
    if form.validate_on_submit():
        # Make sure the user logging in exists
        user = users.User.GetByUsername(form.username.data)
        if user:
            # Make sure the passwords match
            if not user.ValidatePassword(form.password.data):
                errors = 'Incorrect password'
        else:
            errors = 'User %s not found' % (username,)
        if errors:
            flask.flash(errors, 'error')
        else:
            # log the user in via the login system
            if login.login_user(user, remember=bool(form.remember.data)):
                flask.flash('Login Succeeded')
                return flask.redirect(flask.request.args.get('next') or flask.url_for('.user_profile'))
            else:
                flask.flash('Login Error', 'error')
    return flask.render_template('login.html', form=form)


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

@view.route('/create', methods=['GET', 'POST'])
def create_user_page():
    """Create new users."""
    if login.current_user.is_authenticated():
        return flask.redirect(flask.url_for('.user_profile'))
    ok_to_create = False
    form = forms.CreateAccountForm()
    if form.validate_on_submit():
        ok_to_create = True
        # Make sure the username is available
        if form.username.data:
            new_user = users.User.GetByUsername(form.username.data)
        if new_user:
            flask.flash('Username %s is not available.' % (form.username.data,), 'error')
            new_user = None
            ok_to_create = False
        # Make sure the email is not in use
        if form.email.data:
            new_user = users.User.GetByEmail(form.email.data)
            if new_user:
                flask.flash('E-mail address %s is already in use.' % (form.email.data,), 'error')
                new_user = None
                ok_to_create = False
        # Make sure the path is not in use
        if form.blog_path.data:
            new_blog = blogs.Blog.GetByPath(form.blog_path.data)
            if new_blog:
                flask.flash('Blog path %s is not available' % (form.blog_path.data,), 'error')
                new_blog = None
                ok_to_create = False
    if ok_to_create:
        # First create and persist the user.
        new_user = users.User(form.username.data,
                              form.email.data,
                              form.name.data,
                              form.password.data)
        new_user.Persist()
        # Now create and persist the blog.
        new_blog = blogs.Blog(form.blog_path.data,
                              form.blog_name.data,
                              new_user)
        new_blog.Persist()
        flask.flash('Account Created. Please Log In')
        return flask.redirect(flask.url_for('.login_page'))
    # Something failed.  Let the user try again.
    return flask.render_template('create.html', form=form)

@view.route('/reset', methods=['GET', 'POST'])
@login.fresh_login_required
def pw_reset_page():
    """Process a password change request."""
    ok_to_change = True
    form = forms.PasswordResetForm()
    if form.validate_on_submit():
        # Make sure the old password is correct.
        if login.current_user.ValidatePassword(form.old_password.data):
            login.current_user.SetPassword(form.new_password.data)
            login.current_user.Persist()
            flask.flash('Password Updated.')
            return flask.redirect(flask.url_for('.user_profile'))
        else:
            flask.flash('Invalid Password', 'error')
    return flask.render_template('pw_reset.html', form=form)
        
        
