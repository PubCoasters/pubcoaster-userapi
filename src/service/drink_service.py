from flask import request, jsonify
from src.app import db
from src.models.drink import Drink
from uuid import uuid4

class DrinkService():

    def create_drink(self, name):
        uuid = str(uuid4())
        drink = Drink(uuid=uuid, name=name.lower())
        db.session.add(drink)
        db.session.commit()
        return Drink.query.filter_by(uuid=uuid).first()