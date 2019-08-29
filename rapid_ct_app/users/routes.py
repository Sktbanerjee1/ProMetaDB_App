from rapid_ct_app import db, bcrypt
from rapid_ct_app.helpers import save_picture
from rapid_ct_app.files.models import File
from rapid_ct_app.settings import mail

import numpy as np
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_, and_
from flask_mail import Message

from .forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from .models import User

users = Blueprint('users', __name__)

# register
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


# login
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# account
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='assets/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
 
 
# files uploaded by a particular user
@users.route("/files", methods=['GET', 'POST'])
@login_required
def user_uploaded():
    all_files = []
    upload_dates = []
    heatmapdata = {}
    
    file_query = File.query.order_by(File.added_on.desc()).filter_by(user_id = current_user.id)
    
    for item in file_query:
        all_files.append(item)        
    
    
    if len(all_files) == 0:
        flash('No files have been uploaded!', 'danger')
        return redirect(url_for('main.index'))
    else:
        for file in all_files:
            timestamp = file.added_on
            date_added = file.added_on.strftime("%d-%m-%Y")
            upload_dates.append(date_added) 
        pass 
    
        unique_dates = np.unique(upload_dates)
        
        for date in unique_dates:
            date_time = datetime.strptime(date,"%d-%m-%Y")
            timestamp = date_time.timestamp()
            upload_count = File.query.filter_by(date=date, user_id=current_user.id).count() 
            heatmapdata[timestamp] = upload_count
         
        user_bleed_files = File.query.filter_by(sample_type="Bleed(ICH)", user_id=current_user.id)
        user_control_files = File.query.filter_by(sample_type="Control(Normal)", user_id=current_user.id)
        user_other_files = File.query.filter(
            and_(or_(File.sample_type == 'Lesion', File.sample_type == 'Calcification')),File.user_id == current_user.id
        )
        bleed_num = user_bleed_files.count()
        control_num = user_control_files.count()
        others_num = user_other_files.count()
        counts = [
            {'name':"Bleed", 'value':f'{bleed_num}'},
            {'name':"Control", 'value':f'{control_num}'},
            {'name':"Others", 'value':f'{others_num}'}, 
        ]

        return render_template(
            'user_files.html',
            bleed=user_bleed_files,
            control=user_control_files,
            others=user_other_files,
            counts=counts,
            heatmapdata=heatmapdata
        )

# method for constructing password reset email body with reset token
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.'''
    mail.send(msg)


# method for requesting password reset
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


# method for resetting password
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)