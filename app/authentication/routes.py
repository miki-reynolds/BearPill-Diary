from app.authentication import blueprint
from app.authentication.forms import *
from app.models import *
from app.authentication.email_reset_pw import *
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user


@blueprint.route('/register', methods=['GET', 'POST'])
def register_page():
    form = UserForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash("Account successfully created!", category="success")
        return redirect(url_for('home_bp.member_diary'))

    if form.errors != {}: #If there are templates from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating an account: {err_msg}", category="danger")

    # if user somehow get to this page by accident
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.member_diary'))

    return render_template('register.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    # in the case user already logged in but accidentally goes to the login page -> they dont need to login again
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.member_diary'))

    form = LoginForm()
    if form.validate_on_submit():
        attempted_username = User.query.filter_by(username=form.username.data).first()
        if attempted_username and attempted_username.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_username, remember=form.remember_me.data)
            flash(f"Hi {attempted_username.username.capitalize()}, good to see you again :)", category="success")
            return redirect(url_for('home_bp.member_diary'))
        else:
            flash(f"Oh no, the email address and password are not a match :( Please try again!", category="danger")

    return render_template('login.html', title='Log In', form=form)


@blueprint.route('/logout')
def logout_page():
    logout_user()
    flash("You have been successfully logged out!", category="info")
    return redirect(url_for('home_bp.home_page'))


@blueprint.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request_page():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user:
            send_password_reset_email(user)
        flash('Instructions on how to reset the password have been sent to your email!', category='success')
        return redirect(url_for('auth_bp.login_page'))

    # if user somehow get to this page by accident
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.member_diary'))

    return render_template('reset_password_request.html', title='Reset Password Requesr', form=form)


@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_page(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home_bp.home_page'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # set_password is the Flask method
        user.password = form.password1.data
        db.session.commit()
        flash('Password reset successfully!', category='success')
        return redirect(url_for('auth.login'))

    # if user somehow get to this page by accident
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.member_diary'))

    return render_template('reset_password.html', form=form)


