from flask import request, jsonify
from app import db
from models.neighborhood import Neighborhood
from uuid import uuid4

class NeighborhoodService():

    def create_nbhood(self, location_id, neighborhood):
        uuid = str(uuid4())
        nbhood = Neighborhood(uuid=uuid, location_id=location_id, neighborhood=neighborhood.lower())
        db.session.add(nbhood)
        db.session.commit()
        return Neighborhood.query.filter_by(neighborhood=neighborhood.lower(), location_id=location_id).first()