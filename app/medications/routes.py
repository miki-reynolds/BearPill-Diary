from app import db
from app.medications import blueprint
from app.medications.forms import MedForm
from app.models import Meds
from app.utils.helper_functions import*
from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import current_user, login_required
from datetime import datetime


@blueprint.route('/member/medications')
@login_required
def meds_page():
    total_meds = len(current_user.user_meds.all())
    page = request.args.get('page', 1, type=int)
    # paginate() returned-value, has_next, has_prev, prev_num, next_num are attributes
    # from Pagination objections from Flask-SQLAlchemy
    meds = current_user.user_meds.paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    prev_url = url_for('meds_bp.meds_page', page=meds.prev_num) \
        if meds.has_prev else None
    next_url = url_for('meds_bp.meds_page', page=meds.next_num) \
        if meds.has_next else None

    return render_template('meds.html', title='Medications', total_meds=total_meds,
                           meds=meds.items, prev_url=prev_url, next_url=next_url)


@blueprint.route('/member/medications/<int:id>')
@login_required
def med_page(id):
    med = Meds.query.get_or_404(id)
    return render_template('med.html', title='Medication', med=med, id=med.id)


@blueprint.route('/member/medications/add', methods=['POST', 'GET'])
@login_required
def med_add_page():
    form = MedForm()
    if form.validate_on_submit():
        timestamp = datetime.now()
        medname = form.medname.data
        new_med = Meds(medname=medname, dose=form.dose.data, directions=form.directions.data,
                       purpose=form.purpose.data, timestamp=timestamp, notes=form.notes.data,
                       category=form.category.data,
                       user_meds_id=int(current_user.id))
# clear the form after we use it
        form.medname.data = ''
        form.dose.data = ''
        form.directions.data = ''
        form.purpose.data = ''
        form.timestamp.data = timestamp
        form.notes.data = ''
# add med to database
        db.session.add(new_med)
        db.session.commit()
        flash(f"{new_med.medname} successfully added!", category="success")
        return redirect(url_for('meds_bp.meds_page'))

    return render_template('med_add.html', title='Add a New Medication', form=form)


@blueprint.route('/member/medications/<int:id>/update', methods=['POST', 'GET'])
@login_required
def med_update_page(id):
    med_to_update = Meds.query.get_or_404(id)
    form = MedForm()
    if form.validate_on_submit():
        med_to_update.medname = form.medname.data.upper()
        med_to_update.dose = form.dose.data
        med_to_update.directions = form.directions.data
        med_to_update.purpose = form.purpose.data
        form.timestamp.data = med_to_update.timestamp
        med_to_update.notes = form.notes.data
        form.category.data = med_to_update.category

        db.session.add(med_to_update)
        db.session.commit()
        flash(f"{med_to_update.medname} successfully updated :)", category="success")
        return redirect(url_for('meds_bp.med_page', id=med_to_update.id))

    if current_user.id == med_to_update.user_meds_id:
        form.medname.data = med_to_update.medname
        form.dose.data = med_to_update.dose
        form.directions.data = med_to_update.directions
        form.purpose.data = med_to_update.purpose
        form.timestamp.data = med_to_update.timestamp
        form.notes.data = med_to_update.notes
        form.notes.data = med_to_update.category
        return render_template('med_update.html', form=form, id=med_to_update.id)

    return redirect(url_for('meds_bp.meds_page'))


@blueprint.route('/member/medications/<int:id>/delete')
@login_required
def med_delete_page(id):
    med_to_delete = Meds.query.get_or_404(id)
    try:
        db.session.delete(med_to_delete)
        db.session.commit()
        flash("Medication successfully deleted!", category="success")
        return redirect(url_for('meds_bp.meds_page'))
    except:
        flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
        return redirect(url_for('meds_bp.meds_page'))


@blueprint.route('/member/medications/delete')
@login_required
def meds_delete_page():
    try:
        db.session.query(Meds).filter_by(user_meds_id=current_user.id).delete()
        db.session.commit()
        flash("All medications successfully deleted!", category="success")
        return redirect(url_for('meds_bp.meds_page'))
    except:
        flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
        return redirect(url_for('meds_bp.meds_page'))


# todo try to incoporate ways to search for alternate names
# to get med insights from openAPI
@blueprint.route('/member/medications/<int:id>/insights')
def med_insights_page(id):
    med = Meds.query.get_or_404(id)

    med_name = ""
    for letter in med.medname:
        if letter == " ":
            med_name += "+"
        else:
            med_name += letter

    drug_label = ['https://api.fda.gov/drug/label.json?search=openfda.generic_name:', f'"{med_name}"',
                  '+openfda.brand_name:', f'"{med_name}"']
    drug_event = ['https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:', f'"{med_name}"',
                  '+patient.drug.openfda.brand_name:', f'"{med_name}"', '&count=patient.reaction.reactionmeddrapt.exact']

    data_label = med_verify_link(drug_label)
    data_event = med_verify_link(drug_event)
    if data_label:
        return render_template('med_insights.html', title='Medication Insights', med=med,  id=med.id,
                           data_label=med_label(data_label))
    elif data_event:
        return render_template('med_insights.html', title='Medication Insights', med=med, id=med.id,
                           data_event=med_event(data_event))

    elif data_label and data_event:
        return render_template('med_insights.html', title='Medication Insights', med=med, id=med.id,
                           data_label=med_label(data_label), data_event=med_event(data_event))
    else:
        return redirect(url_for('meds_bp.med_page', id=med.id))