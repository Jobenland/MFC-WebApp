import os

basedir = os.path.abspath(os.path.dirname(__file__))

#can leave blank if opt out of secret key option
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '<insert-your-secret-key-here>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SHOW_CAPTCHA = False
    RECAPTCHA_SITE_KEY = '<insert-your-site-key-here>'
    RECAPTCHA_SECRET_KEY = '<insert-your-secret-key-here>'


class DevelopmentConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
