from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from app import db

class User(db.Model):
    __tablename__ = 'user'
    user_name = db.Column(db.String(128), primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    link_to_prof_pic = db.Column(db.Text(16383), nullable=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(256), nullable=True)

    def __init__(self, user_name, email, prof_pic, first_name, last_name, full_name, bio=None):
        self.user_name = user_name
        self.email = email
        if prof_pic is not None:
            self.link_to_prof_pic = prof_pic
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        if bio is not None:
            self.bio = bio