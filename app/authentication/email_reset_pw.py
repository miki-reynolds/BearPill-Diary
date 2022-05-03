from flask import render_template, current_app
from app.email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(subject='[BearPill Diary] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email_address],
               message_body=render_template('reset_password_instructions.txt',
                                         user=user, token=token),
               html_body=render_template('reset_password_instructions.html',
                                         user=user, token=token))