from app import db


class Callforward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exten = db.Column(db.String(4), index=True, unique=True)
    forward_phone = db.Column(db.String(11), index=True, unique=True)
    timeout = db.Column(db.String(4))

    def __init__(self, exten, forward_phone , timeout):
        self.exten = exten
        self.forward_phone = forward_phone
        self.timeout = timeout

    def __repr__(self):
        return '<Exten {}>'.format(self.exten)