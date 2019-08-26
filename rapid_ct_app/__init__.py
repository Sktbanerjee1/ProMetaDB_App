import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dropzone import Dropzone
from flask_mail import Mail


# app init
app = Flask(__name__)

# database init
db = SQLAlchemy(app)


# bcrypt init
bcrypt = Bcrypt(app)

# login_manager init
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


# dropzone init
dropzone = Dropzone(app)


from rapid_ct_app import settings
from rapid_ct_app import template_filters

from rapid_ct_app.users.routes import users
from rapid_ct_app.main.routes import main
from rapid_ct_app.files. routes import files


app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(files)

