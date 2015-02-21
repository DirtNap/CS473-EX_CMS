import datetime
from .. import db

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    path = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)  # Only one blog per user, please

    @staticmethod
    def GetByPath(path):
        return Blog.query.filter_by(path=path).first()

    def __init__(self, path, name, owner):
        self.path = path
        self.name = name
        self.owner_id = owner.id

    def Persist(self):
        if not self.IsPersisted():
            db.session.add(self)
            db.session.commit()

    def IsPersisted(self):
        return (self.id is not None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s: %s (%s)" % (self.name, self.path, self.owner)
