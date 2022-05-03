from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length


class AllergyForm(FlaskForm):
    allergy = StringField(label='Allergies:', validators=[Length(max=255)])
    reactions = StringField(label='Reactions:', validators=[Length(max=255)])
    category = SelectField(label='Category (current or past):', choices=[(1, 'Current'), (2, 'Past')])
    submit = SubmitField(label="Ready to submit?")
