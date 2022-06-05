from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length


class AllergyForm(FlaskForm):
    allergy = StringField(label='Allergies:', validators=[Length(max=255)])
    reactions = StringField(label='Reactions:', validators=[Length(max=255)])
    category = SelectField(label='Category (current or past):', choices=[('Current', 'Current'), ('Past', 'Past')])
    submit = SubmitField(label="Ready to submit?")
