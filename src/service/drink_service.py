from flask import request, jsonify
from src.app import db
from src.models.drink import Drink

class DrinkService():

    def create_drink(self, name):
        drink = Drink(name=name.lower())
        db.session.add(drink)
        db.session.commit()
        return Drink.query.filter_by(name=name.lower()).first()