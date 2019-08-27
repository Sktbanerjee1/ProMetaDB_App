from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import and_, or_
from rapid_ct_app.files.models import File

main = Blueprint('main', __name__)

# landing
@main.route('/')
def landing():
    return render_template('landing.html')


# index
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    all_files = list(File.query.all())
    all_count = len(all_files)
    all_bleed_count = File.query.filter_by(sample_type="Bleed(ICH)").count()
    all_normal_count = File.query.filter_by(sample_type="Control(Normal)").count()
    all_other_files_count = File.query.filter(or_(File.sample_type == 'Lesion', File.sample_type == 'Calcification')).count()
    
    user_bleed_count = File.query.filter_by(sample_type="Bleed(ICH)", user_id=current_user.id).count()
    user_control_files = File.query.filter_by(sample_type="Control(Normal)", user_id=current_user.id).count()
    user_other_files = File.query.filter(
        and_(or_(File.sample_type == 'Lesion', File.sample_type == 'Calcification')),File.user_id == current_user.id
    ).count()

    print(all_count)
    return render_template(
        'index.html',
        all_count=all_count,
        all_bleed_count=all_bleed_count,
        all_normal_count=all_normal_count,
        all_other_files_count=all_other_files_count
    )


# contact
@main.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template('reach-us.html')