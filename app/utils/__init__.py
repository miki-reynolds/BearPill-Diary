from flask import Blueprint


blueprint = Blueprint("utils", __name__,
                      template_folder='templates')


from app.utils import filters, helper_functions