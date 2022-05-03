from flask import Blueprint


blueprint = Blueprint("errors_bp", __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/errors/static')


from app.errors import errors_handlers