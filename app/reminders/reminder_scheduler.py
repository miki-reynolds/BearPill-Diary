from app.reminders.google_api import Create_Service, convert_to_RFC_datetime
import json
import os


CREDENTIALS_JSON = {"web":{"client_id":"990448112960-u8rculh5m9mqvk809qnp5oh7bqkfggfg.apps.googleusercontent.com","project_id":"the-bearpill-diary","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["https://auth0.com/login/callback"],"javascript_origins":["https://auth0.com"]}}


# CLIENT_STR_VAR = os.environ.get('CLIENT_STR_VAR')
with open("google-credentials.json", "w") as ggc:
    json.dump(CREDENTIALS_JSON, ggc, indent=2)

CLIENT_SECRET_FILE = "google-credentials.json"

API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
# http://localhost:8080/


def reminder_template(summary, description, attendee_name, attendee_email, start_date, end_date, freq, freq_interval, freq_byday):
    template = {
        'summary': summary,
        'description': description,
        'colorId': 7,
        'transparency': 'opaque',
        'visibility': 'private',
        'attendees': [
            {
                'displayName': attendee_name,
                'email': attendee_email,
                'organizer': False,
            }
        ],
        'start': {
            'dateTime': convert_to_RFC_datetime(start_date),
            'timeZone': 'UTC'
        },
        'end': {
            'dateTime': convert_to_RFC_datetime(end_date),
            'timeZone': 'UTC'
        },
        'recurrence': [
            # f"RRULE:FREQ={freq};INTERVAL={freq_interval}"
            f"RRULE:FREQ={freq};INTERVAL={freq_interval};BYDAY={freq_byday}"
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 5},
                {'method': 'popup', 'minutes': 5},
            ],
        },
    }
    return template


# create reminder for meds/measurements
def create_reminder(summary, description, attendee_name, attendee_email, start_date, end_date, freq, freq_interval, freq_byday):
    template = reminder_template(summary, description, attendee_name, attendee_email, start_date, end_date, freq, freq_interval, freq_byday)
    reminder = service.events().insert(calendarId='primary', body=template).execute()
    return reminder
    # pass


# update reminder
def update_reminder(event_id, summary, description, attendee_name, attendee_email, start_date, end_date, freq, freq_interval, freq_byday):
    new_template = reminder_template(summary, description, attendee_name, attendee_email, start_date, end_date, freq, freq_interval, freq_byday)
    # service.events().update(calendarId='primary', eventId=event_id, body=new_template).execute()
    # return reminder_to_update
    pass


# delete reminder
def delete_reminder(event_id):
    # service.events().delete(calendarId='primary', eventId=event_id).execute()
    pass


