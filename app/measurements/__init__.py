from flask import Blueprint

blueprint = Blueprint('measurements_bp', __name__,
                      template_folder='templates',
                      static_folder='static')


from app.measurements import routes, forms