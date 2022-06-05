from app.authentication.forms import *
from app.models import *
from app.home import blueprint
from app.home.forms import SearchForm, ContactForm
from app.utils.helper_functions import pagination
from app.email import send_email
from flask import render_template, redirect, url_for, flash, request, g, current_app
from flask_login import current_user, login_required
import os


# to pass the information to navbar
@blueprint.before_app_request
def search_navbar():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@blueprint.route('/search')
@login_required
def search():
    page = request.args.get('page', 1, type=int)
    # get data from the submitted form
    q = g.search_form.q.data

    # query the db
    meds_by_name = Meds.query.filter(Meds.medname.like('%' + q.upper() + '%')).order_by(Meds.medname)
    meds_by_dose = Meds.query.filter(Meds.dose.like('%' + q + '%')).order_by(Meds.medname)
    meds_by_directions = Meds.query.filter(Meds.directions.like('%' + q + '%')).order_by(Meds.medname)
    meds_by_purpose = Meds.query.filter(Meds.purpose.like('%' + q + '%')).order_by(Meds.medname)
    measurements = Measurements.query.filter(Measurements.measurement_name.like('%' + q.upper() + '%')).order_by(Measurements.measurement_name)
    allergies = Allergies.query.filter(Allergies.allergy.like('%' + q.upper() + '%')).order_by(Allergies.allergy)

    total_results = len(meds_by_name.all()) + len(meds_by_dose.all()) + len(meds_by_directions.all()) \
                    + len(meds_by_purpose.all()) + len(measurements.all()) + len(allergies.all())
    next_url = url_for('home_bp.search', q=g.search_form.q.data, page=page + 1) \
        if total_results > (page * current_app.config['ITEMS_PER_PAGE']) else None
    prev_url = url_for('home_bp.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None

    # pagination to get the items per page
    meds_by_name = pagination(meds_by_name, page)
    meds_by_dose = pagination(meds_by_dose, page)
    meds_by_directions = pagination(meds_by_directions, page)
    meds_by_purpose = pagination(meds_by_purpose, page)
    measurements = pagination(measurements, page)
    allergies = pagination(allergies, page)

    return render_template('search.html', q=q, meds_by_name=meds_by_name.items,
                           meds_by_dose=meds_by_dose.items, meds_by_directions=meds_by_directions.items,
                           meds_by_purpose=meds_by_purpose.items, measurements=measurements.items,
                           allergies=allergies.items, next_url=next_url, prev_url=prev_url)


@blueprint.route('/', methods=['POST', 'GET'])
@blueprint.route('/home', methods=['POST', 'GET'])
@blueprint.route('/welcome', methods=['POST', 'GET'])
def home_page():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(subject=form.subject.data, sender=form.email_address.data,
                   recipients=[os.environ.get('MAIL_USERNAME')],
                   message_body=form.message_body.data, html_body=form.message_body.data)
        flash("Successfully sent! :)", category="success")
        return redirect(url_for('home_bp.home_page'))

    return render_template('home.html', title='Home', form=form)


@blueprint.route('/contact', methods=['POST', 'GET'])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(subject=form.subject.data, sender=form.email_address.data,
                   recipients=[os.environ.get('MAIL_USERNAME')],
                   message_body=form.message_body.data, html_body=form.message_body.data)
        flash("Thank you! We'll get back to you soon :)", category="success")
        return redirect(url_for('home_bp.home_page'))

    return render_template('contact.html', title='Contact Form', form=form)


# About Us Page
@blueprint.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html', title='About Us Page')


# Dashboard route where user can see their account info & see their MedDiary summary
@blueprint.route('/member')
@login_required
def member_diary():
    allergies = current_user.user_allergies.all()
    meds = current_user.user_meds.all()
    measurements = current_user.user_measurements.all()
    return render_template('diary.html', title='Member Diary', allergies=allergies, meds=meds, measurements=measurements)


@blueprint.route('/member/dashboard', methods=['POST', 'GET'])
@blueprint.route('/member/settings', methods=['POST', 'GET'])
@login_required
def update_account_page():
    form = UserForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email_address = form.email_address.data
        current_user.password1 = form.password1.data
        current_user.password2 = form.password2.data
        db.session.add(current_user)
        db.session.commit()
        flash("Your account information has been successfully updated! :)", category="success")
        return redirect(url_for('home_bp.home_page'))

    if current_user:
        form.username.data = current_user.username
        form.email_address.data = current_user.email_address

    return render_template('dashboard.html', form=form)


@blueprint.route('/member/dashboard/change_password_request', methods=['POST', 'GET'])
@blueprint.route('/member/settings/change_password_request', methods=['POST', 'GET'])
@login_required
def change_password_request_page():
    form = ChangePasswordRequestForm()

    if form.validate_on_submit() and current_user.check_password_correction(attempted_password=form.password.data):
        token = current_user.get_reset_password_token()
        flash("Ok, let's change the password :)", category="success")
        return redirect(url_for('auth_bp.reset_password_page', token=token))

    return render_template('change_password_request.html', form=form)


@blueprint.route('/member/dashboard/delete_diary', methods=['POST', 'GET'])
@blueprint.route('/member/settings/delete_diary', methods=['POST', 'GET'])
@login_required
def delete_diary():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('home_bp.home_page'))



