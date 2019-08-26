from datetime import datetime
from rapid_ct_app import db

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