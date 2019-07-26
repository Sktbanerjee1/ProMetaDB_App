import os
from rapid_ct_app import app, db, bcrypt
from rapid_ct_app.models import User, Project
from flask import request, render_template, url_for, redirect, abort, jsonify, flash
from rapid_ct_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProjectCreateForm, FileUploadForm
from rapid_ct_app.helpers import save_picture
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


@app.route("/projects", methods=['GET','POST'])
@login_required
def projects():
    user_projects = Project.query.filter_by(user_id=current_user.id)
    all_projects = Project.query.all()
    form = ProjectCreateForm()
    if form.validate_on_submit():
        project = form.project.data
        label = form.label.data
        project_instance = Project(project=project, label=label, user_id=current_user.id)
        db.session.add(project_instance)
        db.session.commit()
        flash(f'project created with name: {project}!', 'success')
        return redirect(url_for('projects'))
    return render_template('projects.html', project_create_form=form, user_projects=user_projects, all_projects=all_projects)



@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('upload.html')
