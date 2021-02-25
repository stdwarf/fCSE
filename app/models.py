from app import db, login
from datetime import datetime
from flask_login import UserMixin

class Callforward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exten = db.Column(db.String(4), index=True, unique=True)
    forward_phone = db.Column(db.String(11), index=True)
    timeout = db.Column(db.String(4))

    def __init__(self, exten, forward_phone , timeout):
        self.exten = exten
        self.forward_phone = forward_phone
        self.timeout = timeout

    def __repr__(self):
        return '<Exten {}>'.format(self.exten)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    fullname = db.Column(db.String(254), index=True)
    email = db.Column(db.String(120), index=True)
    company = db.Column(db.String(254), index=True)
    department = db.Column(db.String(254), index=True)
    title = db.Column(db.String(254), index=True)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.fullname}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))