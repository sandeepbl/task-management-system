import os

# basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'th1s-r34lly-n33ds-t0-b3-ch4ng3d'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:SanjuMtl06@database-tms.czecim0cqbz3.us-east-2.rds.amazonaws.com/task-management-system'
    JWT_SECRET_KEY = 'bd05ce67c2091c6c789e2a27'


class ProductionConfig(DefaultConfig):
    DEBUG = False


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite for testing


config = {
    'default': 'config.DefaultConfig',
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig'
}
