from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length
from datetime import datetime


class MeasurementForm(FlaskForm):
    measurement_name = StringField(label='Measurement Name:', validators=[Length(min=1, max=60), DataRequired()])
    category = SelectField(label='Category:', choices=[('1', 'Single e.g. 80'),
                                                       ('2', 'Double e.g. 80/90'),
                                                       ('3', 'Triple e.g. 80/90/100')])
    submit = SubmitField(label="Ready to submit?")


# Remember IntegerField shouldn't have a Len Requirement
# Single Unit - measurement number contains only one number
class MeasurementSingleForm(FlaskForm):
    number = IntegerField(label='Number:', validators=[DataRequired()])
    timestamp = DateTimeField('Date Added:', default=datetime.now())
    submit = SubmitField(label="Ready to submit?")


# Double Units - measurement number contains 2 numbers: 1upper/1lower
class MeasurementDoubleForm(FlaskForm):
    upper_number = IntegerField(label='Upper Number:', validators=[DataRequired()])
    lower_number = IntegerField(label='Lower Number:', validators=[DataRequired()])
    timestamp = DateTimeField('Date Added:', default=datetime.now())
    submit = SubmitField(label="Ready to submit?")


# Triple Units - measurement number contains 3 numbers: 1st number/2nd number/3rd number (e.g. BP and Pulse)
class MeasurementTripleForm(FlaskForm):
    first_number = IntegerField(label='First Number:', validators=[DataRequired()])
    second_number = IntegerField(label='Second Number:', validators=[DataRequired()])
    third_number = IntegerField(label='Third Number:', validators=[DataRequired()])
    timestamp = DateTimeField('Date Added:', default=datetime.now())
    submit = SubmitField(label="Ready to submit?")

