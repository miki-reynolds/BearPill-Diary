from app import bcrypt, db, login_manager
from flask import current_app
from flask_login import UserMixin
import jwt
from time import time


# to rmb logged-in users when they navigate around the web app
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Create a Model for Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    user_allergies = db.relationship('Allergies', backref='user_allergies', lazy='dynamic')
    user_meds = db.relationship('Meds', backref='user_meds', lazy='dynamic')
    user_measurements = db.relationship('Measurements', backref='user_measurements', lazy='dynamic')

    user_measurements1 = db.relationship('MeasurementSingleNums', backref='user_measurements1', lazy='dynamic')
    user_measurements2 = db.relationship('MeasurementDoubleNums', backref='user_measurements2', lazy='dynamic')
    user_measurements3 = db.relationship('MeasurementTripleNums', backref='user_measurements3', lazy='dynamic')

    user_reminders = db.relationship('Reminders', backref='user_reminders', lazy='dynamic')

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f"{self.username}"


# Create a Model for Medications
class Meds(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    medname = db.Column(db.String(), nullable=False,unique=True)
    dose = db.Column(db.String(), nullable=False)
    directions = db.Column(db.String(), nullable=False)
    purpose = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, nullable=False)
    notes = db.Column(db.String())
    category = db.Column(db.String(), nullable=False)

    user_meds_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    meds_reminders = db.relationship('Reminders', backref='meds_reminders', lazy='dynamic')


    def __repr__(self):
        return f'''
{self.medname.upper()}
{self.dose}
Directions: {self.directions}
Purpose: {self.purpose}
Notes: {self.notes}
'''


# Create a Model for Reminders
class Reminders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    event_id = db.Column(db.String(), nullable=False)
    summary = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=100))
    # add a person to share the event/reminder with
    attendee_name = db.Column(db.String(length=50))
    attendee_email = db.Column(db.String(length=50))
    '''
    The recurrence field contains an array of strings representing one or several RRULE, RDATE or EXDATE
    '''
    # RDATE property: specifies additional dates or date-times when the event occurrences should happen
    start_date = db.Column(db.DateTime, index=True, nullable=False)
    end_date = db.Column(db.DateTime, index=True, nullable=False)

    # RRULE property: rule for repeating the event
    freq = db.Column(db.String())
    freq_interval = db.Column(db.Integer())
    freq_byday = db.Column(db.String(length=100))

    # mapping
    user_reminders_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    meds_reminders_id = db.Column(db.Integer(), db.ForeignKey('meds.id'))
    measurements_reminders_id = db.Column(db.Integer(), db.ForeignKey('measurements.id'))


# Create a Model for Measurements
class Measurements(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    measurement_name = db.Column(db.String(length=100), unique=True, nullable=False)
    category = db.Column(db.String(), nullable=False)
    # mapping the measurement names to users
    user_measurements_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # mapping the measurement numbers to users
    measurement_nums1 = db.relationship('MeasurementSingleNums', backref='measurement_nums1', lazy='dynamic')
    measurement_nums2 = db.relationship('MeasurementDoubleNums', backref='measurement_nums2', lazy='dynamic')
    measurement_nums3 = db.relationship('MeasurementTripleNums', backref='measurement_nums3', lazy='dynamic')
    measurements_reminders = db.relationship('Reminders', backref='measurements_reminders', lazy='dynamic')


# Create a Model for Measurements that contain only 1 number
class MeasurementSingleNums(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer(), index=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, nullable=False)
    # mapping
    user_measurements1_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    measurement_nums1_id = db.Column(db.Integer(), db.ForeignKey('measurements.id'))

    def __repr__(self):
        return f"{self.number}"


# Create a Model for Measurements that contain 2 numbers
class MeasurementDoubleNums(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(), nullable=False)
    upper_number = db.Column(db.Integer(), index=True, nullable=False)
    lower_number = db.Column(db.Integer(), index=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, nullable=False)
    # mapping
    user_measurements2_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    measurement_nums2_id = db.Column(db.Integer(), db.ForeignKey('measurements.id'))

    def __repr__(self):
        return f"{self.upper_number}/{self.lower_number}"


# Create a Model for Measurements that contain 3 numbers
class MeasurementTripleNums(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(), nullable=False)
    first_number = db.Column(db.Integer(), index=True, nullable=False)
    second_number = db.Column(db.Integer(), index=True, nullable=False)
    third_number = db.Column(db.Integer(), index=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, nullable=False)
    # mapping
    user_measurements3_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    measurement_nums3_id = db.Column(db.Integer(), db.ForeignKey('measurements.id'))

    def __repr__(self):
        return f"{self.first_number}/{self.second_number}/{self.third_number}"


# Create a Model for Allergies
class Allergies(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    allergy = db.Column(db.String(length=200), nullable=False)
    reactions = db.Column(db.String(length=200))
    category = db.Column(db.String(), nullable=False)
    # mapping
    user_allergies_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.allergies}"





