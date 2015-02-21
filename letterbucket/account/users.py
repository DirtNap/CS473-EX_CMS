import hashlib
import datetime
from .. import db, login_manager

def GetPasswordHash(password):
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(32), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    blog = db.relationship('Blog', uselist=False,
                           backref='owner', lazy='joined')

    @staticmethod
    @login_manager.user_loader
    def GetById(id):
        result = User.query.get(int(id))
        print result.blog
        return result

    @staticmethod
    def GetByUsername(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def GetByEmail(email):
        return User.query.filter_by(email=email).first()

    def __init__(self, username, email, name, password):
        self.username = username
        self.email = email
        self.name = name
        self.SetPassword(password)

    def ValidatePassword(self, password):
        return self.password_hash == GetPasswordHash(password)

    def SetPassword(self, password):
        self.password_hash = GetPasswordHash(password)

    def Persist(self):
        if not self.IsPersisted():
            db.session.add(self)
        db.session.commit()

    def IsPersisted(self):
        return (self.id is not None)

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username

    def __repr__(self):
        return "user: %s, id: %d, email: %s>" % (self.username,
                                                 self.id,
                                                 self.email)
