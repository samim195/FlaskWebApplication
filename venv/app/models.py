from datetime import datetime
from datetime import date
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'htt[://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    terminal = db.Column(db.Integer, index=True, unique=True)
    serial = db.Column(db.String(120))
    model = db.Column(db.String(128))
    delivered_to_customer = db.Column(db.String(1))
    date_delivered = db.Column(db.String(10))
    returned_to_logistics = db.Column(db.String(1))
    date_returned = db.Column(db.String(10))

    def __repr__(self):
        return '<serial {}>'.format(self.serial)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))