from flask import request, jsonify
from src.app import db
from src.models.neighborhood import Neighborhood

class NeighborhoodService():

    def create_nbhood(self, location_id, neighborhood):
        nbhood = Neighborhood(location_id=location_id, neighborhood=neighborhood.lower())
        db.session.add(nbhood)
        db.session.commit()
        return Neighborhood.query.filter_by(neighborhood=neighborhood.lower(), location_id=location_id).first()