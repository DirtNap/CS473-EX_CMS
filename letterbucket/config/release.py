import base

class ReleaseConfig(base.BaseConfig):
    MYSQL_HOST = 'budb.cajqpq0vcqye.us-east-1.rds.amazonaws.com'
    MYSQL_USER = lbuser
    MYSQL_PASS = None
    SQLALCHEMY_DATABASE_URI = None

    @classmethodn
    def Initialize(cls):
        cls.SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (cls.MYSQL_USER,
                                                               cls.MYSQL_PASS,
                                                               cls.MYSQL_HOST,
                                                               cls.MYSQL_DB)
class DevelopmentConfig(ReleaseConfig):
    MYSQL_DB = letterbucket_dev

class ProductionConfig(ReleaseConfig):
    MYSQL_DB = letterbucket

