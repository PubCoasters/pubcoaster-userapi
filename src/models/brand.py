from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from src.app import db
from uuid import uuid4

class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(128), default=uuid4, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)

    def __init__(self, uuid, name, type):
        self.uuid = uuid
        self.name = name
        self.type = type