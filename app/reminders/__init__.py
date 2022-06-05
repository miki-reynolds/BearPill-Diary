from flask import Blueprint


blueprint = Blueprint('reminders_bp', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/reminders/static')


from app.reminders import forms, reminder_scheduler