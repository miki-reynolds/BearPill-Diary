from app.reminders.google_api import Create_Service, convert_to_RFC_datetime


# http://localhost:8080/
CLIENT_SECRET_FILE = "google-credentials.json"
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES):
    try:
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        return service
    except:
        return "Error!"


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
    try:
        service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        template = reminder_template(summary, description, attendee_name, attendee_email, start_date, end_date, freq, freq_interval, freq_byday)
        reminder = service.events().insert(calendarId='primary', body=template).execute()
        return reminder
    except:
        print("Error!")


# update reminder
def update_reminder(event_id, summary, description, attendee_name, attendee_email, start_date, end_date, freq, freq_interval, freq_byday):
    try:
        service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        new_template = reminder_template(summary, description, attendee_name, attendee_email, start_date, end_date, freq, freq_interval, freq_byday)
        reminder_to_update = service.events().update(calendarId='primary', eventId=event_id, body=new_template).execute()
        return reminder_to_update
    except:
        print("Error!")


# delete reminder
def delete_reminder(event_id):
    try:
        service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        service.events().delete(calendarId='primary', eventId=event_id).execute()
    except:
        print("Error!")

