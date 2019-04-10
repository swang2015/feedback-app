from flask import render_template, Blueprint, url_for, redirect, flash, request, Markup
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from feedback import db, bcrypt
from feedback.model import User
from .forms import LoginForm, RegisterForm
from .confirmation import generate_token, confirm_token, send_email


user_blueprint = Blueprint('usersys', __name__,)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data,
            confirmed=False
        )
        db.session.add(user)
        db.session.commit()

        token = generate_token(user.email)
        confirm_url = url_for('usersys.confirm_email', token=token, _external=True)
        if send_email(user.email, confirm_url):
        	flash('A confirmation email has been sent via email. (user@loblaw.ca may not receive email.)', 'success')
        else:
        	flash('Error occurred while sending confirmation email.', 'danger')

        login_user(user)

        return redirect(url_for('main.start'))

    return render_template('user/register.html', register_user_form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash('Welcome back!', 'success')
            if not user.confirmed:
            	resend_url = url_for('usersys.resend_confirmation')
            	flash(Markup("You haven't confirmed your account yet. Resend confirmation email <a href='"+resend_url+"'>here</a>."), 'warning')
            return redirect(url_for('main.start'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', login_user_form=form)
    return render_template('user/login.html', login_user_form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('main.index'))


@user_blueprint.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account is already confirmed.', 'info')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.start'))


@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_token(current_user.email)
    confirm_url = url_for('usersys.confirm_email', token=token, _external=True)
    if send_email(current_user.email, confirm_url):
        flash('A new confirmation email has been sent.', 'success')
    else:
    	flash('Error occurred while sending confirmation email.', 'danger')
    return redirect(url_for('main.start'))