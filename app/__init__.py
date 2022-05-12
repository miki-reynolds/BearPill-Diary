from flask import Flask, request, current_app
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
login_manager = LoginManager()
# this is to handle pages viewed only by logged-in users
# the 'login' is a function/endpoint without (), similar to how you'd put a function in url_for('')
login_manager.login_view = 'auth_bp.login_page'
login_manager.login_message_category = "info"
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ElasticSearch - have to download separate app/service
    # app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URI']) \
    #     if app.config['ELASTICSEARCH_URI'] else None

    db.init_app(app)
    # migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # create blueprints
    from app.home import blueprint as home_blueprint
    from app.authentication import blueprint as authentication_blueprint
    from app.medications import blueprint as meds_blueprint
    from app.measurements import blueprint as measurements_blueprint
    from app.allergies import blueprint as allergies_blueprint
    from app.errors import blueprint as errors_blueprint
    from app.utils import blueprint as utils_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(meds_blueprint)
    app.register_blueprint(measurements_blueprint)
    app.register_blueprint(allergies_blueprint)
    app.register_blueprint(errors_blueprint)
    app.register_blueprint(utils_blueprint)

    if not app.debug and not app.testing:
        # emails sent to admins in case of errors
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

    return app


from app import models

