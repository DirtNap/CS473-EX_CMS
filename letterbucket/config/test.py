import base

class TestConfig(base.BaseConfig):
    DEBUG = True

class LocalConfig(TestConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (base.BaseConfig.GetFileSystemPath('test.sqlite3', 'datastore'))

class MemoryConfig(TestConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
