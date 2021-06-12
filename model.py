from core import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=True, nullable=False)
    degree = db.Column(db.Float, nullable=False)
    state = db.Column(db.Integer, nullable=False)


class UserCity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cities = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
