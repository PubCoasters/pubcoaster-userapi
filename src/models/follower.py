from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from app import db
from models.user import User

class Follower(db.Model):
    __tablename__ = 'follower'
    follower_user = db.Column(db.String(128), ForeignKey('user.user_name'), primary_key=True)
    following_user = db.Column(db.String(128), ForeignKey('user.user_name'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)
    follower = relationship(
        User,
        backref=backref('follower'),
        foreign_keys=[follower_user],
        uselist=True
    )
    following = relationship(
        User,
        backref=backref('following'),
        foreign_keys=[following_user],
        uselist=True
    )
