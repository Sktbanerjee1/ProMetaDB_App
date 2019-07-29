import os
from datetime import datetime
from rapid_ct_app import app, db, bcrypt
from rapid_ct_app.models import User, Project, File
from flask import request, render_template, url_for, redirect, abort, jsonify, flash
from rapid_ct_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from rapid_ct_app.helpers import save_picture
from rapid_ct_app.settings import upload_path
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
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
    
    
@app.route('/upload', methods=['POST'])
def handle_upload():
    for key, f in request.files.items():
        if key.startswith('file'):
            user_dir_name = f'{current_user.username}'
            user_dir_path = os.path.join(upload_path, user_dir_name)
            
            if os.path.exists(user_dir_path):
                pass
            else:
                try:
                    os.mkdir(user_dir_path)
                except:
                    print('Directory could not be created!')

            user_upload = os.path.join(user_dir_path, f.filename)
            f.save(user_upload)
            
            try:
                file_instance = File(filename=f.filename, path=user_upload, uploader=current_user)
                db.session.add(file_instance)
                db.session.commit()
            except:
                raise Exception('Database entry failed')
            

    return '', 204

        
@app.route('/form', methods=['POST'])
def handle_form():
    flash('Files added successfully!', 'success')
    return redirect(url_for('index'))
       

@app.route("/user/files", methods=['GET', 'POST'])
def uploaded_files():
    user_upload_files = File.query.filter_by(user_id=current_user.id)
    return render_template('user_files.html', user_upload_files=user_upload_files)

