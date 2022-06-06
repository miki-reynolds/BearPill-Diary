from app import db

from app.measurements import blueprint
from app.measurements.forms import MeasurementForm, MeasurementSingleForm, MeasurementDoubleForm, MeasurementTripleForm
from app.models import Measurements, MeasurementSingleNums, MeasurementDoubleNums, MeasurementTripleNums, Reminders

from app.reminders.forms import ReminderForm
from app.reminders.reminder_scheduler import *

from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from datetime import datetime


# Measurements Summary
@blueprint.route('/member/measurements')
@login_required
def measurements_page():
    total_measurements = len(current_user.user_measurements.all())
    page = request.args.get('page', 1, type=int)
    # paginate() returned-value, has_next, has_prev, prev_num, next_num are attributes
    # from Pagination objections from Flask-SQLAlchemy
    measurements = current_user.user_measurements.paginate(
        page, current_app.config['ITEMS_PER_PAGE'], False)
    prev_url = url_for('measurements_bp.measurements_page', page=measurements.prev_num) \
        if measurements.has_prev else None
    next_url = url_for('measurements_bp.measurements_page', page=measurements.next_num) \
        if measurements.has_next else None

    return render_template('measurements.html', total_measurements=total_measurements,
                           measurements=measurements.items, prev_url=prev_url, next_url=next_url)


# Measurement Page with Number Table and Chart
@blueprint.route('/member/measurements/<int:id>')
@login_required
def measurement_page(id):
    measurement = Measurements.query.get(id)
    if measurement.category == '1':
        numbers = measurement.measurement_nums1.all()
        timestamps = [measurement.timestamp.strftime("%m/%d") for measurement in numbers]
        return render_template('measurement.html', measurement=measurement, numbers=numbers, timestamps=timestamps)

    elif measurement.category == '2':
        numbers = measurement.measurement_nums2.all()
        uppernums = [measurement.upper_number for measurement in numbers]
        lowernums = [measurement.lower_number for measurement in numbers]
        timestamps = [measurement.timestamp.strftime("%m/%d") for measurement in numbers]
        return render_template('measurement.html', measurement=measurement, timestamps=timestamps,
                               numbers=numbers, uppernums=uppernums, lowernums=lowernums)

    elif measurement.category == '3':
        numbers = measurement.measurement_nums3.all()
        firstnums = [number.first_number for number in numbers]
        secondnums = [number.second_number for number in numbers]
        thirdnums = [number.third_number for number in numbers]
        timestamps = [measurement.timestamp.strftime("%m/%d") for measurement in numbers]
        return render_template('measurement.html', measurement=measurement, timestamps=timestamps, numbers=numbers,
                               firstnums=firstnums, secondnums=secondnums, thirdnums=thirdnums)


# Add Measurement
@blueprint.route('/member/measurements/add', methods=['POST', 'GET'])
@login_required
def measurement_add_page():
    form = MeasurementForm()
    if form.validate_on_submit():
        measurement_name = form.measurement_name.data.upper()
        measurement_to_add = Measurements.query.filter_by(measurement_name=measurement_name).first()

        # in case no measurement category exists in the measurement list
        if measurement_to_add is None:
            new_measurement = Measurements(measurement_name=form.measurement_name.data.upper(),
                                           category=form.category.data,
                                           user_measurements_id=current_user.id)
            # clear the form after we use it
            form.measurement_name.data = ''
            # add med to database
            db.session.add(new_measurement)
            db.session.commit()
            flash(f"Ok, let's move on to the specifics!", category="success")
            # redirect to the appropriate category for the measurement
            if new_measurement.category == '1':
                return redirect(url_for('measurements_bp.measurement_add_single_page', id=new_measurement.id))
            elif new_measurement.category == '2':
                return redirect(url_for('measurements_bp.measurement_add_double_page', id=new_measurement.id))
            elif new_measurement.category == '3':
                return redirect(url_for('measurements_bp.measurement_add_triple_page', id=new_measurement.id))

        # if measurement category exists, new numbers can be added directly
        if measurement_to_add.category == '1':
            return redirect(url_for('measurements_bp.measurement_add_single_page', id=measurement_to_add.id))
        elif measurement_to_add.category == '2':
            return redirect(url_for('measurements_bp.measurement_add_double_page', id=measurement_to_add.id))
        elif measurement_to_add.category == '3':
            return redirect(url_for('measurements_bp.measurement_add_triple_page', id=measurement_to_add.id))

    return render_template('measurement_add.html', title='Add Measurements', form=form)


# Add Single Measurement
@blueprint.route('/member/measurements/add/<int:id>/single', methods=['POST', 'GET'])
@login_required
def measurement_add_single_page(id):
    numbers_to_add = Measurements.query.get_or_404(id)
    timestamp = datetime.now()
    form = MeasurementSingleForm()
    if form.validate_on_submit():
        new_measurement_number = MeasurementSingleNums(category=numbers_to_add.category,
                                                       number=form.number.data,
                                                       timestamp=timestamp,
                                                       user_measurements1_id=current_user.id,
                                                       measurement_nums1_id=numbers_to_add.id)
        db.session.add(new_measurement_number)
        db.session.commit()
        # clear the form after we use it
        form.number.data = ''
        form.timestamp = timestamp

        flash(f"New number successfully added to {numbers_to_add.measurement_name} category!", category="success")
        return redirect(url_for('measurements_bp.measurements_page'))

    return render_template('measurement_add_single.html', title='Add Single Numbers', form=form)


# Add Double Measurement
@blueprint.route('/member/measurements/add/<int:id>/double', methods=['POST', 'GET'])
@login_required
def measurement_add_double_page(id):
    numbers_to_add = Measurements.query.get_or_404(id)
    timestamp = datetime.now()
    form = MeasurementDoubleForm()
    if form.validate_on_submit():
        new_measurement_number = MeasurementDoubleNums(category=numbers_to_add.category,
                                                       upper_number=form.upper_number.data,
                                                       lower_number=form.lower_number.data,
                                                       timestamp=timestamp,
                                                       user_measurements2_id=current_user.id,
                                                       measurement_nums2_id=numbers_to_add.id)
        db.session.add(new_measurement_number)
        db.session.commit()
        # clear the form after we use it
        form.upper_number.data = ''
        form.lower_number.data = ''
        form.timestamp = timestamp

        flash(f"New number successfully added to {numbers_to_add.measurement_name} category!", category="success")
        return redirect(url_for('measurements_bp.measurements_page'))

    return render_template('measurement_add_double.html', title='Add Double Numbers', form=form)


# Add Triple Measurement
@blueprint.route('/member/measurements/add/<int:id>/triple', methods=['POST', 'GET'])
@login_required
def measurement_add_triple_page(id):
    numbers_to_add = Measurements.query.get_or_404(id)
    timestamp = datetime.now()
    form = MeasurementTripleForm()
    if form.validate_on_submit():
        new_measurement_number = MeasurementTripleNums(category=numbers_to_add.category,
                                                       first_number=form.first_number.data,
                                                       second_number=form.second_number.data,
                                                       third_number=form.third_number.data,
                                                       timestamp=timestamp,
                                                       user_measurements3_id=current_user.id,
                                                       measurement_nums3_id=numbers_to_add.id)
        db.session.add(new_measurement_number)
        db.session.commit()
        # clear the form after we use it
        form.first_number.data = ''
        form.second_number.data = ''
        form.third_number.data = ''
        form.timestamp = timestamp

        flash(f"New number successfully added to {numbers_to_add.measurement_name} category!", category="success")
        return redirect(url_for('measurements_bp.measurements_page'))

    return render_template('measurement_add_triple.html', title='Add Triple Numbers', form=form)


# Update Measurement
@blueprint.route('/member/measurements/<int:id>/update')
@login_required
def measurement_update_page(id):
    measurement_to_update = Measurements.query.get_or_404(id)
    form = MeasurementForm()
    # to update the existing form
    if form.validate_on_submit():
        measurement_to_update.measurement_name = form.measurement_name.data.upper()
        measurement_to_update.category = form.category.data
        db.session.add(measurement_to_update)
        db.session.commit()
        flash(f"{measurement_to_update.measurement_name} successfully updated :)", category="success")
        return redirect(url_for('measurements_bp.measurement_page', id=measurement_to_update.id))

    # to have current info filled in the form
    if current_user.id == measurement_to_update.user_measurements_id:
        form.measurement_name.data = measurement_to_update.measurement_name
        form.category.data = measurement_to_update.category
        return render_template('measurement_update.html', form=form)

    return redirect(url_for('measurements_bp.measurements_page'))


# Update Single Measurement
@blueprint.route('/member/measurements/update/single/<int:id>', methods=['POST', 'GET'])
@login_required
def measurement_update_single_page(id):
    num_to_update = MeasurementSingleNums.query.get_or_404(id)
    form = MeasurementSingleForm()
    if form.validate_on_submit():
        num_to_update.number = form.number.data
        num_to_update.timestamp = form.timestamp.data
        db.session.add(num_to_update)
        db.session.commit()
        # clear the form after we use it
        form.number.data = ''
        flash(f"Number successfully edited.", category="success")
        return redirect(url_for('measurements_bp.measurement_page', id=num_to_update.measurement_nums1_id))

    if current_user.id == num_to_update.user_measurements1_id:
        form.number.data = num_to_update.number
        form.timestamp.data = num_to_update.timestamp
        return render_template('measurement_update_single.html', form=form, id=id)

    return redirect(url_for('measurements_bp.measurements_page'))


# Update Double Measurement
@blueprint.route('/member/measurements/update/double/<int:id>', methods=['POST', 'GET'])
@login_required
def measurement_update_double_page(id):
    num_to_update = MeasurementDoubleNums.query.get_or_404(id)
    form = MeasurementDoubleForm()
    if form.validate_on_submit():
        num_to_update.upper_number = form.upper_number.data
        num_to_update.lower_number = form.lower_number.data
        num_to_update.timestamp = form.timestamp.data
        db.session.add(num_to_update)
        db.session.commit()
        # clear the form after we use it
        form.upper_number.data= ''
        form.lower_number.data= ''
        flash(f"Number successfully edited.", category="success")
        return redirect(url_for('measurements_bp.measurement_page', id=num_to_update.measurement_nums2_id))

    if current_user.id == num_to_update.user_measurements2_id:
        form.upper_number.data = num_to_update.upper_number
        form.lower_number.data = num_to_update.lower_number
        form.timestamp.data = num_to_update.timestamp
        return render_template('measurement_update_double.html', form=form, id=id)

    return redirect(url_for('measurements_bp.measurements_page'))


# Update Triple Measurement
@blueprint.route('/member/measurements/update/triple/<int:id>', methods=['POST', 'GET'])
@login_required
def measurement_update_triple_page(id):
    num_to_update = MeasurementTripleNums.query.get_or_404(id)
    form = MeasurementTripleForm()
    if form.validate_on_submit():
        num_to_update.first_number = form.first_number.data
        num_to_update.second_number = form.second_number.data
        num_to_update.third_number = form.third_number.data
        num_to_update.timestamp = form.timestamp.data
        db.session.add(num_to_update)
        db.session.commit()
        # clear the form after we use it
        form.first_number.data = ''
        form.second_number.data = ''
        form.third_number.data = ''
        flash(f"Number successfully edited.", category="success")
        return redirect(url_for('measurements_bp.measurement_page', id=num_to_update.measurement_nums3_id))

    if current_user.id == num_to_update.user_measurements3_id:
        form.first_number.data = num_to_update.first_number
        form.second_number.data = num_to_update.second_number
        form.third_number.data = num_to_update.third_number
        form.timestamp.data = num_to_update.timestamp
        return render_template('measurement_update_triple.html', form=form, id=id)

    return redirect(url_for('measurements_bp.measurements_page'))


# Delete Specific Number on Specific Measurement
@blueprint.route('/member/measurements/<name>/delete/<int:id>')
@login_required
def measurement_delete_number_page(name, id):
    measurement = Measurements.query.filter_by(measurement_name=name).first()
    category = measurement.category
    if measurement:
        if category == '1':
            num1_to_del = MeasurementSingleNums.query.get_or_404(id)
            db.session.delete(num1_to_del)
            db.session.commit()
        elif category == '2':
            num2_to_del = MeasurementDoubleNums.query.get_or_404(id)
            db.session.delete(num2_to_del)
            db.session.commit()
        elif category == '3':
            num3_to_del = MeasurementSingleNums.query.get_or_404(id)
            db.session.delete(num3_to_del)
            db.session.commit()

        flash("Measurement successfully deleted!", category="success")
        return redirect(url_for('measurements_bp.measurement_page', id=measurement.id))
    else:
        flash("Whoops, some unexpected error has occurred... Please try again :(")
        return redirect(url_for('measurements_bp.measurements_page'))


# Delete Measurement
@blueprint.route('/member/measurements/<int:id>/delete')
@login_required
def measurement_delete_page(id):
    measurement_to_del = Measurements.query.get_or_404(id)
    category = measurement_to_del.category
    try:
        if category == '1':
            db.session.query(MeasurementSingleNums).filter_by(measurement_nums1_id=measurement_to_del.id).delete()
            db.session.commit()
        elif category == '2':
            db.session.query(MeasurementDoubleNums).filter_by(measurement_nums2_id=measurement_to_del.id).delete()
            db.session.commit()
        elif category == '3':
            db.session.query(MeasurementTripleNums).filter_by(measurement_nums3_id=measurement_to_del.id).delete()
            db.session.commit()

        db.session.delete(measurement_to_del)
        db.session.commit()
        flash("Measurement successfully deleted!", category="success")
        return redirect(url_for('measurements_bp.measurements_page'))
    except:
        flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
        return redirect(url_for('measurements_bp.measurements_page'))


# Delete Measurements
@blueprint.route('/member/measurements/delete')
@login_required
def measurements_delete_page():
    try:
        db.session.query(Measurements).filter_by(user_measurements_id=current_user.id).delete()
        db.session.query(MeasurementSingleNums).filter_by(user_measurements1_id=current_user.id).delete()
        db.session.query(MeasurementDoubleNums).filter_by(user_measurements2_id=current_user.id).delete()
        db.session.query(MeasurementTripleNums).filter_by(user_measurements3_id=current_user.id).delete()

        db.session.commit()
        flash("All measurements successfully deleted!", category="success")
        return redirect(url_for('measurements_bp.measurements_page'))
    except:
        flash("Whoops, some unexpected error has occurred... Please try again :(")
        return redirect(url_for('measurements_bp.measurements_page'))


# Create reminder
@blueprint.route('/member/measurements/<int:id>/reminders', methods=['POST', 'GET'])
@login_required
def measurement_add_reminder_page(id):
    measurement_to_remind = Measurements.query.get_or_404(id)
    form = ReminderForm()
    if form.validate_on_submit():
        form.summary.data = measurement_to_remind.measurement_name
        summary = measurement_to_remind.measurement_name
        description = form.description.data
        attendee_name = current_user.username if form.attendee_name.data == "" else form.attendee_name.data
        attendee_email = current_user.email_address if form.attendee_email.data == "" else form.attendee_email.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        freq = form.freq.data
        freq_interval = form.freq_interval.data

        # stringtify freq_byday (list)
        freq_byday = ",".join([str(day) for day in form.freq_byday.data])

        # create reminder
        reminder_to_create = create_reminder(summary, description, start_date, end_date,
                                             attendee_name, attendee_email,
                                             freq, freq_interval, freq_byday)

        # adding reminder to database
        try:
            reminder_to_add_to_db = Reminders(event_id=reminder_to_create['id'],
                                        summary=summary, description=description,
                                        attendee_name=attendee_name, attendee_email=attendee_email,
                                        start_date=start_date, end_date=end_date,
                                        freq=freq, freq_interval=freq_interval, freq_byday=freq_byday,
                                        user_reminders_id=current_user.id,
                                        measurements_reminders_id=measurement_to_remind.id)
            # add reminder to database
            db.session.add(reminder_to_add_to_db)
            db.session.commit()

            flash(f"Successfully set up reminder for {measurement_to_remind.measurement_name}!", category="success")
            return redirect(url_for('measurements_bp.measurements_page'))

        except:
            flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
            return redirect(url_for('measurements_bp.measurements_page'))

    form.summary.data = measurement_to_remind.measurement_name

    return render_template('reminder_add.html', title='Create Reminder', form=form)


# Update reminder
@blueprint.route('/member/measurements/reminders/<int:id>', methods=['POST', 'GET'])
@login_required
def measurement_update_reminder_page(id):
    reminder_to_update = Reminders.query.get_or_404(id)
    form = ReminderForm()
    if form.validate_on_submit():
        summary = reminder_to_update.summary
        description = form.description.data
        attendee_name = form.attendee_name.data
        attendee_email = form.attendee_email.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        freq = form.freq.data
        freq_interval = form.freq_interval.data
        # stringtify freq_byday (list)
        freq_byday = ",".join([str(day) for day in form.freq_byday.data])

        # update reminder GG
        try:
            reminder_to_update_in_gg = update_reminder(reminder_to_update.event_id, summary, description,
                                                       attendee_name, attendee_email, start_date, end_date,
                                                       freq, freq_interval, freq_byday)

            # updating reminder in database
            reminder_to_update_in_db = Reminders(event_id=reminder_to_update['id'],
                                        summary=summary, description=description,
                                        attendee_name=attendee_name, attendee_email=attendee_email,
                                        start_date=start_date, end_date=end_date,
                                        freq=freq, freq_interval=freq_interval, freq_byday=freq_byday,
                                        user_reminders_id=current_user.id,
                                        measurements_reminders_id=reminder_to_update.id)

            db.session.add(reminder_to_update_in_db)
            db.session.commit()

            flash(f"{reminder_to_update.summary} successfully updated :)", category="success")
            return redirect(url_for('measurements_bp.measurement_page'))

        except:
            flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
            return redirect(url_for('measurements_bp.measurements_page'))

    if current_user.id == reminder_to_update.user_reminders_id:
        form.summary.data = reminder_to_update.summary
        form.description.data = reminder_to_update.description
        form.attendee_name.data = reminder_to_update.attendee_name
        form.attendee_email.data = reminder_to_update.attendee_email
        form.start_date.data = reminder_to_update.start_date
        form.end_date.data = reminder_to_update.end_date
        form.freq.data = reminder_to_update.freq
        form.freq_interval.data = reminder_to_update.freq_interval
        form.freq_byday.data = reminder_to_update.freq_byday
        return render_template('reminder_update.html', form=form, id=reminder_to_update.id)

    return redirect(url_for('measurements_bp.measurements_page'))


# Delete individual reminder
@blueprint.route('/member/measurements/reminders/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def measurement_delete_reminder_page(id):
    reminder_to_delete = Reminders.query.get_or_404(id)
    try:
        delete_reminder(reminder_to_delete.event_id)
        db.session.delete(reminder_to_delete)
        db.session.commit()
        flash("Reminder successfully deleted!", category="success")
        return redirect(url_for('measurements_bp.measurements_page'))
    except:
        flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
        return redirect(url_for('measurements_bp.measurements_page'))


# Delete all reminders
@blueprint.route('/member/measurements/<int:id>/reminders/delete', methods=['POST', 'GET'])
@login_required
def measurement_delete_reminders_page(id):
    measurement_to_delete_reminders = Measurements.query.get_or_404(id)
    reminders = measurement_to_delete_reminders.measurements_reminders.all()
    try:
        if reminders:
            for reminder in reminders:
                delete_reminder(reminder.event_id)
        db.session.query(Reminders).filter_by(summary=measurement_to_delete_reminders.measurement_name).delete()
        db.session.commit()
        flash(f"All {measurement_to_delete_reminders.measurement_name}'s reminders successfully deleted!", category="success")
        return redirect(url_for('measurements_bp.measurement_page', id=measurement_to_delete_reminders.id))
    except:
        flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
        return redirect(url_for('measurements_bp.measurements_page'))
