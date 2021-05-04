from flask import request, jsonify
from src.app import db
from src.models.brand import Brand
from uuid import uuid4

class BrandService():

    def create_brand(self, name, type_brand):
        uuid = str(uuid4())
        brand = Brand(uuid=uuid, name=name.lower(), type=type_brand.lower())
        db.session.add(brand)
        db.session.commit()
        return Brand.query.filter_by(uuid=uuid).first()