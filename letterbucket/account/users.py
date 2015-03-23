import hashlib
import datetime
from .. import db, login_manager

def GetPasswordHash(password):
    """Get the md5 encoded hash of an arbitrary string, for use as a password.

    Arguments:
      password:  an arbitrary string to encode.

    Returns:  a string (hex digest) representation of the md5 hash of password.
    """
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

class User(db.Model):
    """Represents a user model in the database, and satisfies the user interface for login."""
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
        """Given a representation of the user id, gets the user object.

        Arguments:
          id:  A representation of the id which can be consumed by int()
        Returns:  A User object with the primary key id, or None
        """
        return User.query.get(int(id))

    @staticmethod
    def GetByUsername(username):
        """Get the user by the username.

        Arguments:
          username:  The username of the user.

        Returns:  A User object with that username, or None
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def GetByEmail(email):
        """Get the user by the email.

        Arguments:
          email:  The email of the user.

        Returns:  A User object with that email, or None
        """
        return User.query.filter_by(email=email).first()

    def __init__(self, username, email, name, password):
        """Create a new user.

        Note:  This user is not persisted to the database until Persist()
               is explicitly called.

        Arguments:
          username:  the desired username for the user.  Must be unique.
          email:  the email of the account holder.  Must be unique.
          name:  the display name for this user.  Required.
          password:  An arbitrary password string.  Required.
        """
        self.username = username
        self.email = email
        self.name = name
        self.SetPassword(password)

    def ValidatePassword(self, password):
        """Compares a plaintext password to the stored password hash.

        Arguments:
          password:  A plaintext password to validate

        Returns:  A boolean indicating whether the password produces the same
                  hash as the stored password hash.
        """
        return self.password_hash == GetPasswordHash(password)

    def SetPassword(self, password):
        """Set the internal password hash to a representation of a password.

        Arguments:
          password:  A plaintext password
        """
        if not password:
            raise ValueError('Password can not be empty.')
        self.password_hash = GetPasswordHash(password)

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
        """Indicates whether the user has been persisted.

        Returns:  boolean indicating whether the user was persisted.
        """
        return (self.id is not None)

    def get_id(self):
        """Gets the unicode representation of the user id.

        This is required by the Flask-login user interface.

        Returns:  a unicode integer representation.
        """
        return unicode(self.id)

    def is_active(self):
        """Indicates whether the user is active.

        This is required by the Flask-login user interface.  

        Returns:  boolean if the user is allowed to use the system once authenticated.
        """
        # TODO(dirtnap): Make this dynamic when privileges are implemented.
        return True

    def is_anonymous(self):
        """Indicates that this is a known user.

        This is required by the Flask-login user interface.

        Returns:  False.  This is an immutable method.  Anonymous users are
                  represented by a different user class.
        """
        return False

    def is_authenticated(self):
        """Indicates that this is a logged-in user.

        This is required by the Flask-login user interface.

        Returns:  True.  This is an immutable method.  Anonymous users are
                  represented by a different user class.
        """
        return True

    def __str__(self):
        return self.username

    def __repr__(self):
        return "user: %s, id: %d, email: %s>" % (self.username,
                                                 self.id,
                                                 self.email)
