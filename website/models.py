from . import db  # Importing the db created in __init__.py which is just the SQLAlchemy() object
from flask_login import UserMixin
from sqlalchemy.sql import func

#Database model for notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Database model for users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user (since users can have the same name etc)
    email = db.Column(db.String(150), unique=True)  # no two users can have the same email
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

