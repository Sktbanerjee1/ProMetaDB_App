import os
import secrets
from PIL import Image
from rapid_ct_app import app
from rapid_ct_app.models import Project, File
from flask_login import current_user

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/assets/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

class ProjectChoicesIter(object):
    def __iter__(self):
        user_projects = Project.query.filter_by(user_id=current_user.id)
        for project in user_projects:
            key_val_pair = (project.project, project.project)
            yield key_val_pair


class FileChoicesIter(object):
    def __iter__(self):
        user_files =File.query.filter_by(user_id=current_user.id)
        for file in user_files:
            key_val_pair = (file.filename, file.filename)
            yield key_val_pair
