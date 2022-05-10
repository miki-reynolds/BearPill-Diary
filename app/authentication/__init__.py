from flask import Blueprint


blueprint = Blueprint('auth_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

from app.authentication import routes, forms, email_reset_pw