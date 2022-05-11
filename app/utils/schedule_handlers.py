from flask import render_template, current_app
from app.email import send_email
from apscheduler.schedulers.background import BackgroundScheduler


# send reminders to take meds/measurements to users' emails
def send_reminder(user, item_name):
    send_email(subject='[BearPill Diary] Reminder',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email_address],
               message_body=render_template('reminder.txt', user=user, item=item_name),
               html_body=render_template('reminder_email.html', user=user, item=item_name))


# for scheduling reminders in the background
scheduler = BackgroundScheduler(daemon=True)

