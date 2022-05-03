from app.authentication.forms import *
from app.models import *
from app.home import blueprint
from app.home.forms import*
from app.utils.helper_functions import pagination
from flask import render_template, redirect, url_for, flash, request, g, current_app
from flask_login import current_user, login_required


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
    meds_by_name = Meds.query.filter(Meds.medname.like('%' + q + '%')).order_by(Meds.medname)
    meds_by_dose = Meds.query.filter(Meds.dose.like('%' + q + '%')).order_by(Meds.medname)
    meds_by_directions = Meds.query.filter(Meds.directions.like('%' + q + '%')).order_by(Meds.medname)
    meds_by_purpose = Meds.query.filter(Meds.purpose.like('%' + q + '%')).order_by(Meds.medname)
    measurements = Measurements.query.filter(Measurements.measurement_name.like('%' + q + '%')).order_by(Measurements.measurement_name)
    allergies = Allergies.query.filter(Allergies.allergy.like('%' + q + '%')).order_by(Allergies.allergy)

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


@blueprint.route('/')
@blueprint.route('/home')
@blueprint.route('/welcome')
def home_page():
    return render_template('home.html', title='Home')


@blueprint.route('/contact')
def contact_page():
    return render_template('contact.html', title='Contact Form')


# Dashboard route where user can see their account info & see their MedDiary summary
@blueprint.route('/member')
@login_required
def member_diary():
    allergies = current_user.user_allergies.all()
    meds = current_user.user_meds.all()
    measurements = current_user.user_measurements.all()
    return render_template('diary.html', title='Member Diary', allergies=allergies, meds=meds, measurements=measurements)


@blueprint.route('/dashboard', methods=['POST', 'GET'])
@login_required
def update_account_page():
    form = UserForm()
    id = current_user.id
    user_to_update = User.query.get_or_404(id)

    # update profile info
    if request.method == "POST":
        user_to_update.username = request.form["username"]
        user_to_update.email_address = request.form["email_address"]
        db.session.commit()
        flash("Your account information has been successfully updated! :)", category="success")
        return render_template('dashboard.html', form=form, user_to_update=user_to_update, id=id, current_user=current_user)

    # if the method is request, we just wanna pass the current info in the page
    else:
        return render_template('dashboard.html', form=form, user_to_update=user_to_update, id=id, current_user=current_user)
