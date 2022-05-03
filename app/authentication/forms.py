from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError


class UserForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
# first() because it either has 0-F or 1-T.
        if user:
            raise ValidationError('This username already exists :( Please try another one.')

    def validate_email(self, email_to_check):
        email_address = User.query.filter_by(email_address=email_to_check.data).first()
        if email_address:
            raise ValidationError('This email address already exists :( Please try another one.')

    username = StringField(label="Username:", validators=[Length(min=6, max=30), DataRequired()])
    email_address = StringField(label="Email Address:", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Create Diary")


class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    remember_me = BooleanField(label="Remember me")
    submit = SubmitField(label="Sign In")


class ResetPasswordRequestForm(FlaskForm):
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Reset Password')


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField(label='Password', validators=[DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Ready to Reset Password?')



