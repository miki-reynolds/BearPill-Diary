from flask import Blueprint

blueprint = Blueprint('home_bp', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/home/static')


from app.home import routes