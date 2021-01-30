from flask import request, jsonify
from src.app import db
from src.models.brand import Brand

class BrandService():

    def create_brand(self, name, type):
        brand = Brand(name=name.lower(), type=type.lower())
        db.session.add(brand)
        db.session.commit()
        return Brand.query.filter_by(name=name.lower(), type=type.lower()).first()