from flask import render_template, request, Blueprint
from flask_login import login_required

main = Blueprint('main', __name__)


# index
@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


# about
@main.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template('reach-us.html')