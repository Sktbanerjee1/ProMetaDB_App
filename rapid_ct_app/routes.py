
# library imports

import os
import io
import pydicom
import matplotlib.pyplot as plt
import numpy as np
from flask.views import View
from sqlalchemy import or_, and_
from datetime import datetime
from matplotlib.figure import Figure
from flask_mail import Message
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import request, render_template, url_for, redirect, abort, jsonify, flash, abort, Response
from flask_login import login_user, current_user, logout_user, login_required

# rapid_ct_app imports

from rapid_ct_app import app, db, bcrypt
from rapid_ct_app.models import User, File
from rapid_ct_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdateFileForm, RequestResetForm, ResetPasswordForm 
from rapid_ct_app.helpers import save_picture
from rapid_ct_app.settings import upload_path, mail


# routes for the RAPID-CT app

# index
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


# about
@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html')


# register
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# account
@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='assets/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
    
# add files
def add_file(target_dir_name, sample_class):
    for key, f in request.files.items():
        if key.startswith('file'):
            filename = f.filename
            current_username = str(current_user.username)
            user_dir = os.path.join(upload_path, current_username)
            
            if os.path.exists(user_dir):
                pass
            else:
                try:
                    os.mkdir(user_dir)
                except:
                    raise Exception("Could not be created! already exists!")
            
            path = os.path.join(user_dir, target_dir_name)

            if os.path.exists(path):
                pass
            else:
                try:
                    os.mkdir(path)
                except:
                    raise Exception("Could not be created! already exists")

            file_path = os.path.join(path, filename)
            file_instance = File(filename=filename, path=file_path, sample_type=sample_class, user_id=current_user.id)
            db.session.add(file_instance)
            db.session.commit()
            f.save(file_path)


# upload bleed files       
@app.route('/add-bleed', methods=['POST'])
def add_bleed():
    sample_class = "Bleed(ICH)"
    target_dir_name = "Bleed"
    try:
        add_file(target_dir_name, sample_class)
    except:
        raise Exception('Uploading to Bleed failed')
    return '', 204



# upload control files
@app.route('/add-control', methods=['POST'])
def add_control():
    sample_class =  "Control(Normal)"
    target_dir_name = "Control"
    try:
        add_file(target_dir_name, sample_class)
    except:
        raise Exception('Uploading to Control failed')
    return '', 204



# upload lesion files
@app.route('/add-lesion', methods=['POST'])
def add_lesion():
    sample_class =  "Lesion"
    target_dir_name = "Lesion"
    try:
        add_file(target_dir_name, sample_class)
    except:
        raise Exception('Uploading to Control failed')
    return '', 204



# upload calcification files
@app.route('/add-calcification', methods=['POST'])
def add_calcification():
    sample_class =  "Calcification"
    target_dir_name = "Calcification"
    try:
        add_file(target_dir_name, sample_class)
    except:
        raise Exception('Uploading to Control failed')
    return '', 204




# files uploaded by a particular user
@app.route("/files", methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
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



# route for a specific file
@app.route("/file/<int:file_id>", methods=['GET', 'POST'])
@login_required
def file(file_id):
    file = File.query.get_or_404(file_id)
    file_size = os.stat(file.path).st_size
    form = UpdateFileForm()
    form.sample_type.data = file.sample_type
    file_path = file.path
    return render_template('file.html', file=file, size=file_size, form=form)


# method to update sample_type of an uploaded file
@app.route("/file/<int:file_id>/update", methods=['POST'])
@login_required
def file_update(file_id):
    form = UpdateFileForm()
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        flash('403 Unauthorized Method', 'danger')
        return redirect(url_for('file', file_id=file.id))
    else:
        if form.validate_on_submit():
            file.sample_type = form.sample_type.data 
            db.session.commit()
            flash(f'Annotation updated!', 'success')
        return redirect(url_for('file', file_id=file.id))
        

# method to delete an uploaded file
@app.route("/file/<int:file_id>/delete", methods=['POST'])
@login_required
def file_delete(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        flash('403 Unauthorized Method', 'danger')
        return redirect(url_for('file', file_id=file.id))
    else:
        os.remove(file.path)
        db.session.delete(file)
        db.session.commit()
        flash('File deleted!', 'success')
        return redirect(url_for('user_uploaded'))


# method for constructing password reset email body with reset token
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.'''
    mail.send(msg)


# method for requesting password reset
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


# method for resetting password
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)