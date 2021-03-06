from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    email_address = EmailField(label="Email Address", validators=[DataRequired()])
    subject = SelectField(choices=[("[Contact] Support", "Support"),
                                   ("[Contact] Feedback", "Feedback"),
                                   ("[Contact] Collaboration Opportunities", "Collaboration Opportunities"),
                                   ("[Contact] Others", "Others")])
    message_body = TextAreaField(label="More Details", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class SearchForm(FlaskForm):
    # q stands for query, a standard way of doing in, e.g. https://www.google.com/search?q=python
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


