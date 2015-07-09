import os

print(os.environ['APP_SETTINGS'])
# print(os.environ['DATABASE_URL'])


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/grap3'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Users/hannes/grap3_test.db'
    # app.config['TESTING'] = True
    # app.config['WTF_CSRF_ENABLED'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    #     'sqlite:///Users/hannes/tmp/test.db'
