import flask_wtf
import wtforms
import wtforms.validators

class LoginForm(flask_wtf.Form):
    username = wtforms.StringField('Username',
                                   validators=[wtforms.validators.Length(min=3, max=32, message='Username must be betweeen 3 and 32 characters'),
                                   wtforms.validators.InputRequired(message='Username Required'),
                                   wtforms.validators.regexp(r'^[A-Za-z0-9_@\-\.]+$', message='Invalid Username')])
    password = wtforms.PasswordField('Password',
                                     validators=[wtforms.validators.InputRequired(),
                                     wtforms.validators.Length(min=5)])
    remember = wtforms.BooleanField('Remember Me')
    submit = wtforms.SubmitField('Log In')
                                    
class PasswordResetForm(flask_wtf.Form):
    old_password = wtforms.PasswordField('Old Password',
                                         validators=[wtforms.validators.InputRequired()])

    new_password = wtforms.PasswordField('New Password',
                                         validators=[wtforms.validators.InputRequired(),
                                         wtforms.validators.Length(min=5)])
    repeat_password = wtforms.PasswordField('Password',
                                            validators=[wtforms.validators.InputRequired(),
                                            wtforms.validators.EqualTo('new_password',
                                            message='Passwords must match.')])
    submit = wtforms.SubmitField('Reset Password')
    
class CreateAccountForm(flask_wtf.Form):
    username = wtforms.StringField('Username',
                                   validators=[wtforms.validators.Length(min=3, max=32, message='Username must be betweeen 3 and 32 characters'),
                                   wtforms.validators.InputRequired(message='Username Required'),
                                   wtforms.validators.regexp(r'^[A-Za-z0-9_@\-\.]+$', message='Invalid Username')])
    name = wtforms.StringField('Name', validators=[wtforms.validators.InputRequired(),
                               wtforms.validators.Length(min=3, max=128)])
    email = wtforms.StringField('E-Mail:', validators=[wtforms.validators.InputRequired(),
                                wtforms.validators.Email()]);
    password = wtforms.PasswordField('Password',
                                     validators=[wtforms.validators.InputRequired(),
                                     wtforms.validators.Length(min=5)])
    blog_name = wtforms.StringField('Blog Name',
                                    validators=[wtforms.validators.InputRequired(),
                                    wtforms.validators.Length(min=2, max=256)])
    blog_path = wtforms.StringField('Blog Path',
                                    validators=[wtforms.validators.InputRequired(),
                                    wtforms.validators.Length(min=1, max=64),
                                    wtforms.validators.regexp(r'^[A-Za-z0-9_\.\-]+$')])
