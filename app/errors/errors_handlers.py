from app import db
from app.errors import blueprint
from flask import render_template


# instead of using @app.errorhandler, use the bp one to make it more independent of the app

@blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@blueprint.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


