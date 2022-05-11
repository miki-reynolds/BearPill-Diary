from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import NumberRange


# form for setting up reminders to take meds/measurements
class ReminderForm(FlaskForm):
    months = IntegerField(label='Month Frequency/Specific Month/Range:', validators=[NumberRange(min=1, max=12)], default=1)
    weeks = IntegerField(label='Week Frequency/Specific Week/Range', validators=[NumberRange(min=1, max=53)], default=1)
    day_of_the_week = SelectField(label='Day of the Week', choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'),
                                                                 (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')])
    days_freq = IntegerField(label='Day Frequency/Specific Day/Range', validators=[NumberRange(min=1, max=31)], default=1)
    hours = IntegerField(label='Time', validators=[NumberRange(min=0, max=23)], default=8)
    minutes = IntegerField(label='@Minutes', validators=[NumberRange(min=0, max=59)], default=30)

    submit = SubmitField(label="Ready to submit?")

