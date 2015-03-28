import flask_wtf
import wtforms
import wtforms.validators

class PostForm(flask_wtf.Form):
    title = wtforms.StringField('Post Title',
                                validators=[wtforms.validators.InputRequired(message='Post Title Required')])
    body = wtforms.PasswordField('Content',
                                     validators=[wtforms.validators.InputRequired(message='')])
    submit = wtforms.SubmitField('Submit')
