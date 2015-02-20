import hashlib
from .. import db, login_manager

def GetPasswordHash(password):
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(32), nullable=False)

    @staticmethod
    @login_manager.user_loader
    def GetById(id):
        User.get(int(id))

    @staticmethod
    def GetByUsername(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def GetByEmail(email):
        return User.query.filter_by(email=email).first()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = GetPasswordHash(password)

    def validate_password(self, password):
        return self.password_hash == GetPasswordHash(password)

    def is_persisted(self):
        return (self.id is None)

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
