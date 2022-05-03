from app.allergies import blueprint
from app.allergies.forms import *
from app.models import *
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required


@blueprint.route('/member/allergies')
@login_required
def allergies_page():
    total_allergies = len(current_user.user_allergies.all())
    # to get the page number from the links(explicit, implicit)
    page = request.args.get('page', 1, type=int)
    # paginate() returned-value, has_next, has_prev, prev_num, next_num are attributes
    # from Pagination objections from Flask-SQLAlchemy
    allergies = current_user.user_allergies.paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    prev_url = url_for('allergies_bp.allergies_page', page=allergies.prev_num) \
        if allergies.has_prev else None
    next_url = url_for('allergies_bp.allergies_page', page=allergies.next_num) \
        if allergies.has_next else None

    return render_template('allergies.html', title='Allergies', total_allergies=total_allergies,
                           allergies=allergies.items, prev_url=prev_url, next_url=next_url)


@blueprint.route('/member/allergies/add', methods=['POST', 'GET'])
@login_required
def allergy_add_page():
    form = AllergyForm()
    if form.validate_on_submit():
        new_allergy = Allergies(allergy=form.allergy.data, reactions=form.reactions.data,
                       category=form.category.data, user_allergies_id=int(current_user.id))
# clear the form after we use it
        form.allergy.data = ''
        form.reactions.data = ''
# add med to database
        db.session.add(new_allergy)
        db.session.commit()
        flash(f"{new_allergy.allergy} successfully added!", category="success")
        return redirect(url_for('allergies_bp.allergies_page'))

    return render_template('allergy_add.html', title='Add a New Allergy', form=form)


@blueprint.route('/member/allergies/<int:id>/update', methods=['POST', 'GET'])
@login_required
def allergy_update_page(id):
    allergy_to_update = Allergies.query.get_or_404(id)
    form = AllergyForm()
    if form.validate_on_submit():
        allergy_to_update.allergy = form.allergy.data
        allergy_to_update.reactions = form.reactions.data
        allergy_to_update.category = form.category.data

        db.session.add(allergy_to_update)
        db.session.commit()
        flash(f"Allergies successfully updated :)", category="success")
        return redirect(url_for('allergies_bp.allergies_page'))

    if current_user.id == allergy_to_update.user_allergies_id:
        form.allergy.data = allergy_to_update.allergy
        form.reactions.data = allergy_to_update.reactions
        form.category.data = allergy_to_update.category
        return render_template('allergy_update.html', title='Update Allergy', form=form, id=allergy_to_update.id)

    return redirect(url_for('allergies_bp.allergies_page'))


@blueprint.route('/member/allergies/<int:id>/delete')
@login_required
def allergy_delete_page(id):
    allergy_to_delete = Allergies.query.get_or_404(id)
    try:
        db.session.delete(allergy_to_delete)
        db.session.commit()
        flash("Allergy successfully deleted!", category="success")
        return redirect(url_for('allergies_bp.allergies_page'))
    except:
        flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
        return redirect(url_for('allergies_bp.allergies_page'))


@blueprint.route('/member/allergies/delete')
@login_required
def allergies_delete_page():
    try:
        db.session.query(Allergies).filter_by(user_allergies_id=current_user.id).delete()
        db.session.commit()
        flash("All allergies successfully deleted!", category="success")
        return redirect(url_for('home_bp.member_diary'))
    except:
        flash("Whoops, some unexpected error has occurred... Please try again :(", category="danger")
        return redirect(url_for('home_bp.member_diary'))

