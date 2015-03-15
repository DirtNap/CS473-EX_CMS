import datetime
from .. import db

class PostStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    posts_in_status = db.relationship('Post', backref='status')

    def __new__(cls, code, *args, **kwargs):
        self = cls.GetStatusByCode(code)
        if not self:
            self = super(PostStatus, cls).__new__(cls, code, *args, **kwargs)
        return self

    def __init__(self, code, description=None):
        self.code = code.upper()
        if description:
            self.description = description
            
    @staticmethod
    def GetStatusByCode(code):
        return PostStatus.query.filter_by(code=code.upper()).first()

    def __str__(self):
        return self.code

    def __repr__(self):
        if self.id:
            return '%s:  %s (id=%d)' % (self.code, self.description, self.id)
        return '%s:  %s' % (self.code, self.description)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text,nullable=False)
    create_date = db.Column(db.DateTime,nullable=False)
    post_date = db.Column(db.DateTime)
    pub_date = db.Column(db.DateTime)
    status_id = db.Column(db.Integer, db.ForeignKey('post_status.id'))
    last_modified_by = db.Column(db.Integer,nullable=True)
    last_modified_date = db.Column(db.DateTime)
        

        
    def __init__():
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return '%s: %s (%s)' % (self.name, self.path, self.owner)

        
