from rapid_ct_app import db
from rapid_ct_app.settings import upload_path

from .models import File
from .forms import UpdateFileForm

import os
from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from flask_login import current_user, login_required


files = Blueprint('files', __name__)


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
@files.route('/add-bleed', methods=['POST'])
def add_bleed():
    sample_class = "Bleed(ICH)"
    target_dir_name = "Bleed"
    try:
        add_file(target_dir_name, sample_class)
    except:
        raise Exception('Uploading to Bleed failed')
    return '', 204



# upload control files
@files.route('/add-control', methods=['POST'])
def add_control():
    sample_class =  "Control(Normal)"
    target_dir_name = "Control"
    try:
        add_file(target_dir_name, sample_class)
    except:
        raise Exception('Uploading to Control failed')
    return '', 204



# upload lesion files
@files.route('/add-lesion', methods=['POST'])
def add_lesion():
    sample_class =  "Lesion"
    target_dir_name = "Lesion"
    try:
        add_file(target_dir_name, sample_class)
    except:
        raise Exception('Uploading to Control failed')
    return '', 204



# upload calcification files
@files.route('/add-calcification', methods=['POST'])
def add_calcification():
    sample_class =  "Calcification"
    target_dir_name = "Calcification"
    try:
        add_file(target_dir_name, sample_class)
    except:
        raise Exception('Uploading to Control failed')
    return '', 204



# route for a specific file
@files.route("/file/<int:file_id>", methods=['GET', 'POST'])
@login_required
def file(file_id):
    file = File.query.get_or_404(file_id)
    file_size = os.stat(file.path).st_size
    form = UpdateFileForm()
    form.sample_type.data = file.sample_type
    file_path = file.path
    return render_template('file.html', file=file, size=file_size, form=form)


# method to update sample_type of an uploaded file
@files.route("/file/<int:file_id>/update", methods=['POST'])
@login_required
def file_update(file_id):
    form = UpdateFileForm()
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        flash('403 Unauthorized Method', 'danger')
        return redirect(url_for('files.file', file_id=file.id))
    else:
        if form.validate_on_submit():
            file.sample_type = form.sample_type.data 
            db.session.commit()
            flash(f'Annotation updated!', 'success')
        return redirect(url_for('files.file', file_id=file.id))
        

# method to delete an uploaded file
@files.route("/file/<int:file_id>/delete", methods=['POST'])
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
        return redirect(url_for('users.user_uploaded'))
