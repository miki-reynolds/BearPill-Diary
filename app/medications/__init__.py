from flask import Blueprint


blueprint = Blueprint('meds_bp', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/medications/static')


from app.medications import routes, forms