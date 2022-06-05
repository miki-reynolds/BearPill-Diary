from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()

# Handle pages viewed only by logged-in users
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login_page'
login_manager.login_message_category = "info"
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    from app.home import blueprint as home_blueprint
    from app.authentication import blueprint as authentication_blueprint
    from app.medications import blueprint as meds_blueprint
    from app.measurements import blueprint as measurements_blueprint
    from app.allergies import blueprint as allergies_blueprint
    from app.reminders import blueprint as reminders_blueprint
    from app.errors import blueprint as errors_blueprint
    from app.utils import blueprint as utils_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(meds_blueprint)
    app.register_blueprint(measurements_blueprint)
    app.register_blueprint(allergies_blueprint)
    app.register_blueprint(reminders_blueprint)
    app.register_blueprint(errors_blueprint)
    app.register_blueprint(utils_blueprint)

    if not app.debug and not app.testing:
        # Emails sent to admins in case of errors
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='BearPills Project Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Heroku
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/bearpills.log', maxBytes=10240, backupCount=10)

            # format the output to logs
            # %(asctime)s adds the time of creation of the LogRecord
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s'
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        # levels above info will be included as well (main levels debug(), info(), warning(), error(), and critical())
        app.logger.setLevel(logging.INFO)
        app.logger.info('BearPills Startup')

    return app


from app import models
