from dotenv import load_dotenv
from os import path, environ

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY') or '1f7d46f72fff29293ec462cc'
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # pagination
    ITEMS_PER_PAGE = 10
    # search functionality (more complex)
    # ELASTICSEARCH_URI = environ.get('ELASTICSEARCH_URI')

    # for heroku
    LOG_TO_STDOUT = environ.get('LOG_TO_STDOUT')

    # for error-handling and sending reminder email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 or 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'thebearpillproject@gmail.com'
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    ADMINS = ['thebearpillproject@gmail.com']



class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

