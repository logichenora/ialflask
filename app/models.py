from datetime import datetime
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #tests = db.relationship('Test', backref='tester', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Region {}>'.format(self.name)

    def dto(self):
        dto = {}
        dto['id'] = self.id
        dto['name'] = self.name
        dto['color'] = self.color
        return dto

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
