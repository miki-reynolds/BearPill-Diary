from flask import Blueprint


blueprint = Blueprint('allergies_bp', __name__,
                      template_folder='templates',
                      static_folder='static')


from app.allergies import routes, forms