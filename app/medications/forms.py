from app.models import Meds
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime


class MedForm(FlaskForm):
    def validate_medication(self, medname_to_check):
        medname = Meds.query.filter_by(medname=medname_to_check.data).first()
        if medname:
            raise ValidationError('This medication already exists in your diary!')

    medname = StringField(label='Medication Name:', validators=[Length(min=2, max=100), DataRequired()])
    dose = StringField(label='Dosage:', validators=[Length(min=2, max=100), DataRequired()])
    directions = StringField(label='Directions:', validators=[Length(min=2, max=200), DataRequired()])
    purpose = StringField(label='Purpose:')
    timestamp = DateTimeField(label='Date Added:', default=datetime.now())
    notes = StringField(label='Notes:')
    category = SelectField(label='Category (current or past):', choices=[('Current', 'Current'), ('Past', 'Past')])
    submit = SubmitField(label="Ready to submit?")


