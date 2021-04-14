from flask import request, jsonify
from app import db
from models.brand import Brand

class BrandService():

    def create_brand(self, name, type_brand):
        brand = Brand(name=name.lower(), type=type_brand.lower())
        db.session.add(brand)
        db.session.commit()
        return Brand.query.filter_by(name=name.lower(), type=type_brand.lower()).first()