from app.models import Meds
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField
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
    timestamp = DateTimeField('Date Added:', default=datetime.now())
    notes = StringField(label='Notes:')
    category = SelectField(label='Category (current or past):', choices=[(1, 'Current'), (2, 'Past')])
    submit = SubmitField(label="Ready to submit?")


class SearchForm(FlaskForm):
    # q = query, a standard way of doing in, e.g. https://www.google.com/search?q=python
    q = StringField(label='Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        # request.args to get the field values in the query string via GET method
        # as we don't have a submit button here (if sumit, then request.form)
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args

        # if csrf_enabled, disable it to bypass the CSRF validation
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

