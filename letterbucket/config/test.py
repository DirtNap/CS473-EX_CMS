import base

class TestConfig(base.BaseConfig):
    """A base config for other testing configs."""
    DEBUG = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False

class LocalConfig(TestConfig):
    """A configuration object for using a local SQLite3 database."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (base.BaseConfig.GetFileSystemPath('test.sqlite3', 'datastore'))

class MemoryConfig(TestConfig):
    """A configuration object for using an in-memory SQLite3 database."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
