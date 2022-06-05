from app.models import Meds
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, SelectMultipleField, EmailField, DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput

from datetime import datetime


# create checkbox field for multi-select
class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=True)
    option_widget = CheckboxInput()


class ReminderForm(FlaskForm):
    summary = StringField(label='Reminder:', validators=[Length(min=2, max=100), DataRequired()])
    description = StringField(label='Description:', validators=[Length(max=100)], default="Empty :)")
    # add a person to share the event/reminder with
    attendee_name = StringField(label="Person's Name:")
    attendee_email = EmailField(label="Person's Email:")
    '''
    The recurrence field contains an array of strings representing one or several RRULE, RDATE or EXDATE
    '''
    # RDATE property: specifies additional dates or date-times when the event occurrences should happen
    start_date = DateTimeField(label='Start Date & Time:', default=datetime.now())
    end_date = DateTimeField(label='End Date & Time:', default=datetime.now())

    # RRULE property: rule for repeating the event
    freq = SelectField(label='Frequency', choices=[('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly')])
    freq_interval = IntegerField(label='Interval', default=1)
    freq_byday = MultiCheckboxField(label='Week Days:', choices=[('MO', 'Monday'), ('TU', 'Tuesday'),
                                                                  ('WE', 'Wednesday'), ('TH', 'Thursday'),
                                                                  ('FR', 'Friday'), ('SA', 'Saturday'), ('SU', 'Sunday')],
                                    default='MO,TU,WE,TH,FR,SA,SU')
    submit = SubmitField(label="Ready to submit?")


