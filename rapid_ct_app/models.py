from datetime import datetime
from rapid_ct_app import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    files = db.relationship('File', backref='uploader', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    added_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date = db.Column(db.String(55), nullable=False, default=datetime.utcnow().strftime("%d-%m-%Y"))
    filename = db.Column(db.String(55), nullable=False)
    path = db.Column(db.String(120), nullable=False)
    sample_type = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"('{self.filename}', '{self.added_on}', '{self.path}', {self.sample_type})"