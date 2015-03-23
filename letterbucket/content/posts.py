from .. import db
import datetime

class PostStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    posts_in_status = db.relationship('Post', backref='status')

    def __new__(cls, code=None, * args, ** kwargs):
        self = None
        if code:
            self = cls.GetByCode(code)
        if not self:
            self = super(PostStatus, cls).__new__(cls, code, * args, ** kwargs)
        return self

    def __init__(self, code, description=None):
        self.code = code.upper()
        if description:
            self.description = description

    @staticmethod
    def GetById(id):
        """Get the post status which resides at the given id.

        Arguments:
          id:  the id of the post status.

        Returns:  the PostStatus object with the primary key id, or None
        """
        return PostStatus.query.get(int(id))

    @staticmethod
    def GetByCode(code):
        """Get the post status which resides at the given code.

        Arguments:
          code:  the code of the post status.

        Returns:  the PostStatus object with the corresponding code, or None
        """
        return PostStatus.query.filter_by(code=code.upper()).first()

    def __str__(self):
        return self.code

    def __repr__(self):
        if self.id:
            return '%s:  %s (id=%d)' % (self.code, self.description, self.id)
        return '%s:  %s' % (self.code, self.description)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    post_date = db.Column(db.DateTime)
    pub_date = db.Column(db.DateTime)
    status_id = db.Column(db.Integer, db.ForeignKey('post_status.id'))
    last_modified_by = db.Column(db.Integer, nullable=True)
    last_modified_date = db.Column(db.DateTime)

    @staticmethod
    def GetById(id):
        """Get the post which resides at the given id.

        Arguments:
          id:  the id of the post.

        Returns:  the Post object with the primary key id, or None
        """
        return Post.query.get(int(id))

    @staticmethod
    def GetByBlogId(id):
        """Get the post which resides at the given blog id.

        Arguments:
          id:  the blog id of the post.

        Returns:  the Post objects with the corresponding blog id, or None
        """
        return Post.query.filter_by(blog_id=id).all()

    @staticmethod
    def GetByBlogPath(path):
        """Get the post which resides at the given blog path.

        Arguments:
          path:  the blog path of the post.

        Returns:  the Post objects with the corresponding blog path, or None
        """
        blog = blogs.Blog.GetByPath(path)
        return Post.query.filter_by(blog_id=blog.id).all()

    def __init__(self, blog, title, body, status=None):
        """Create a new post.

        Note:  This post is not persisted to the database until Persist()
               is explicitly called.

        Arguments:
          blog: The Blog of the post. The Blog must be persisted.
          title:  The desired title for display of the post.
          body:  The body for the post.
        """
        self.blog = blog
        self.title = title
        self.body = body
        if not status:
          self.status = PostStatus('Draft')
        else:
          self.status = status

    def __str__(self):
        return self.name

    def __repr__(self):
        return '%s: %s (%s)' % (self.name, self.path, self.owner)
