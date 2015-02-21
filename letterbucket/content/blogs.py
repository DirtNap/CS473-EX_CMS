import datetime
from .. import db

class Blog(db.Model):
    """Represents a blog model in the database."""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    path = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)  # Only one blog per user, please

    @staticmethod
    def GetByPath(path):
        """Get the blog which resides at the given path.

        Arguments:
          path:  the path of the blog.

        Returns:  the Blog object with the corresponding path, or None
        """
        return Blog.query.filter_by(path=path).first()

    def __init__(self, path, name, owner):
        """Create a new blog.

        Note:  This blog is not persisted to the database until Persist()
               is explicitly called.

        Arguments:
          path:  The desired path for display of the blog.  Must be unique.
          name:  The name for the blog.
          owner:  A User object who owns the blog.  The User must be persisted.
        """
        self.path = path
        self.name = name
        self.owner_id = owner.id

    def Persist(self, db_session=None):
        """Store the current version of the user in the database.

        NOTE:  This method commits the database session given by
               db_session.  By default, this will be the session at
               db.session.  If this transaction should be isolated,
               an explicitly created session must be provided.

        Arguments:
          db_session:  Optional.  A Flask SQLAlchemy session to use.
        """
        if not db_session:
            db_session = db.session
        if not self.IsPersisted():
            db_session.add(self)
        db_session.commit()

    def IsPersisted(self):
        """Indicates whether the blog has been persisted.

        Returns:  boolean indicating whether the blog was persisted.
        """
        return (self.id is not None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s: %s (%s)" % (self.name, self.path, self.owner)
