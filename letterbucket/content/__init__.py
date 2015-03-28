import flask
from flask.ext import login

import blogs
import posts
import forms

from .. import db

# View for content.
view = flask.Blueprint('blogs', __name__, template_folder='templates')

@view.route('/edit', methods=['GET', 'POST'], defaults={'post_id':None})
@view.route('/edit/<int:post_id>', methods=['GET'])
@login.login_required
def edit_post(post_id):
    title, content = (None, None)
    if post_id:
        post = posts.Post.GetById(post_id)
        title = post.title
        content = post.body
    form = forms.PostForm(title=title, content=content)
    if form.validate_on_submit():
        if form.post_id.data:
            post = posts.Post.GetById(form.post_id.data)
            post.title = form.post_title.data
            post.body = form.post_input.data
            post.last_modified_date = datetime.datetime.utcnow()
            post.last_modified_by = lgoin.current_user.id
        else:
            post = posts.Post(login.current_user.blog,
                              form.post_title.data,
                              form.post_input.data
            )
            db.session.add(post)
        post.status = posts.PostStatus('Published')
        db.session.commit()
        flask.flash('Published Post %d for blog %s' % (post.id,post.blog.name))
    return flask.render_template('edit_post.html', form=form)
