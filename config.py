from dotenv import load_dotenv
from os import path, environ


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    # CSRF purpose
    SECRET_KEY = environ.get('SECRET_KEY') or "secret"

    # Heroku hasn't updated the postgres, which SQLAlchemy stopped supporting
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # pagination
    ITEMS_PER_PAGE = 10

    # Heroku
    LOG_TO_STDOUT = environ.get('LOG_TO_STDOUT')

    # Error-handling and sending reminder email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 or 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    ADMINS = [environ.get('ADMINS')]


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

