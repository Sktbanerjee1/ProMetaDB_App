import os
from rapid_ct_app import app
from flask_login import current_user

basedir = os.path.abspath(os.path.dirname(__file__))
upload_path = os.path.join(basedir, 'uploads') #only for dev # change to mounted drive in prod

# check if the upload folder exists otherwise create

if os.path.exists(upload_path):
    pass
else:
    try:
        os.mkdir(upload_path)
    except:
        raise Exception('Upload directory error!')


# global config
app.config.update(
    SECRET_KEY='8e791c70866d596a66fa98e9daca396684514915',
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db',
    UPLOADED_PATH=os.path.abspath(upload_path),    
)

# dropzone config
app.config.update(
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='image/*, .dcm',
    DROPZONE_MAX_FILE_SIZE=1024, 
    DROPZONE_MAX_FILES=20,
    DROPZONE_TIMEOUT=5 * 60 * 1000,
    DROPZONE_REDIRECT_VIEW='user_uploaded'
)