import os
from datetime import datetime
from rapid_ct_app import app, db, bcrypt
from rapid_ct_app.models import User, File
from flask import request, render_template, url_for, redirect, abort, jsonify, flash
from rapid_ct_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from rapid_ct_app.helpers import save_picture
from rapid_ct_app.settings import upload_path
from flask_login import login_user, current_user, logout_user, login_required
from flask.views import View
from sqlalchemy import or_
import numpy as np

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


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
    

       
@app.route('/add-bleed', methods=['POST'])
def add_bleed():
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
            
            bleed_path = os.path.join(user_dir, 'ICH')

            if os.path.exists(bleed_path):
                pass
            else:
                try:
                    os.mkdir(bleed_path)
                except:
                    raise Exception("Could not be created! already exists")

            file_path = os.path.join(bleed_path, filename)
            file_instance = File(filename=filename, path=file_path, sample_type="Bleed(ICH)", user_id=current_user.id)
            db.session.add(file_instance)
            db.session.commit()
            f.save(file_path)
    return '', 204

@app.route('/add-control', methods=['POST'])
def add_control():
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
            
            control_path = os.path.join(user_dir, 'Control')

            if os.path.exists(control_path):
                pass
            else:
                try:
                    os.mkdir(control_path)
                except:
                    raise Exception("Could not be created! already exists")

            file_path = os.path.join(control_path, filename)
            file_instance = File(filename=filename, path=file_path, sample_type="Control(Normal)", user_id=current_user.id)
            db.session.add(file_instance)
            db.session.commit()
            f.save(file_path)
    return '', 204

@app.route('/add-lesion', methods=['POST'])
def add_lesion():
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
            
            lesion_path = os.path.join(user_dir, 'Lesion')

            if os.path.exists(lesion_path):
                pass
            else:
                try:
                    os.mkdir(lesion_path)
                except:
                    raise Exception("Could not be created! already exists")

            file_path = os.path.join(lesion_path, filename)
            file_instance = File(filename=filename, path=file_path, sample_type="Lesion", user_id=current_user.id)
            db.session.add(file_instance)
            db.session.commit()
            f.save(file_path)
    return '', 204

@app.route('/add-calcification', methods=['POST'])
def add_calcification():
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
            
            calcification_path = os.path.join(user_dir, 'Calcification')

            if os.path.exists(calcification_path):
                pass
            else:
                try:
                    os.mkdir(calcification_path)
                except:
                    raise Exception("Could not be created! already exists")

            file_path = os.path.join(calcification_path, filename)
            file_instance = File(filename=filename, path=file_path, sample_type="Calcification", user_id=current_user.id)
            db.session.add(file_instance)
            db.session.commit()
            f.save(file_path)
    return '', 204


@app.route("/files", methods=['GET', 'POST'])
@login_required
def user_uploaded():
    user_all_files = []
    upload_dates = []
    
    file_query = File.query.filter_by(user_id = current_user.id)
    
    for item in file_query:
        user_all_files.append(item)        
    
    
    if len(user_all_files) == 0:
        flash('No files have been uploaded!', 'warning')
        return redirect(url_for('index'))
    else:
        for file in user_all_files:
            upload_dates.append(file.added_on.strftime("%d-%m-%Y")) 
        pass 
     
        unique_dates = np.unique(upload_dates)   
        
        for date in unique_dates: 
            upload_count = File.query.filter_by(date=date).count() 
            print(date, upload_count) 
        
        
        
        
        user_bleed_files = File.query.filter_by(sample_type="Bleed(ICH)", user_id=current_user.id)
        user_control_files = File.query.filter_by(sample_type="Control(Normal)", user_id=current_user.id)
        user_other_files = File.query.filter(or_(File.sample_type == 'Lesion', File.sample_type == 'Calcification'))
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
            counts=counts
            
        )




