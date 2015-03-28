import flask_wtf
import wtforms
import wtforms.validators

class PostForm(flask_wtf.Form):
    post_id = wtforms.HiddenField('Post ID')
    post_title = wtforms.StringField('Post Title',
                                     validators=[wtforms.validators.InputRequired(message='Post Title Required')])
    post_input = wtforms.TextAreaField('Content',
                                       validators=[wtforms.validators.InputRequired(message='Post can not be blank')])
    submit = wtforms.SubmitField('Published')

    def __init__(self, id=None, title=None, content=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if id:
            self.post_id.value = id
        if title:
            self.post_title.value = title
        if content:
            self.post_input.value = content
