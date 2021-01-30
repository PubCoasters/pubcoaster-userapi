from flask import request, jsonify
from src.app import db
from src.models.bar import Bar
from src.models.brand import Brand
from src.models.drink import Drink
from src.models.user import User
from src.models.user_bar import UserBar
from src.models.user_brand import UserBrand
from src.models.user_drink import UserDrink
from src.service.bar_service import BarService as bar_service
from src.service.neighborhood_service import NeighborhoodService as neighborhood_service
from src.service.drink_service import DrinkService as drink_service
from src.service.brand_service import BrandService as brand_service
from sqlalchemy import func

class UserService():


    def create_user_bar(self, body):
        user = body['username']
        bar = body['bar']
        try:
            user_bar = None
            bar_data = Bar.query.filter_by(name=bar.lower()).first()
            if bar_data is None: # no such bar exists in our database - create
                location_data = Location.query.filter_by(location=body['location']).first()
                if 'neighborhood' in body: # neighborhood specified
                    nbhood_data = Neighborhood.query.filter_by(neighborhood=body['neighborhood'].lower()).first()
                    if nbhood_data is not None: # neighborhood exists - create bar with it
                        bar_data = bar_service().create_bar(bar_name=bar.lower(), location_id=location_data.id, neighborhood_id=nbhood_data.id)
                    else: # neighborhood does not exist - create it and then create bar
                        nbhood_data = neighborhood_service().create_nbhood(location_id=location_data.id, neighborhood=body['neighborhood'])
                        bar_data = bar_service().create_bar(bar_name=bar, location_id=location_data.id, neighborhood_id=nbhood_data.id)
                else: # no neighborhood specified - create bar without neighborhood
                    bar_data = bar_service().create_bar(bar_name=bar, location_id=location_data.id)
                bar_id = bar_data.id
                user_bar = UserBar(user_name=user.lower(), bar_id=bar_id)
            else: # bar exists in our database
                bar_id = bar_data.id
                user_bar = UserBar(user_name=user.lower(), bar_id=bar_id)
            db.session.add(user_bar)
            db.session.commit()
            return jsonify({'statusCode': 200, 'message': 'user-bar association successfully created'})
        except Exception as e:
            print(e)
            return jsonify({'statusCode': 500, 'message': 'unable to create new user-bar association'})


    def create_user_brand(self, body):
        user = body['username']
        brand = body['brand']
        print('user:', user, "brand:", brand)
        print('type:', body['type'])
        try:
            user_brand = None
            brand_data = Brand.query.filter_by(name=brand.lower()).first()
            if brand_data is None: # no such brand exists in our database - create
                brand = brand_service.create_brand(brand, body['type']) # TODO: are they always gonna be sending in type?
                user_brand = UserBrand(user_name=user.lower(), brand_id = brand.id)
            else: # brand exists in our database
                brand_id = brand_data.id
                user_brand = UserBrand(user_name=user.lower(), brand_id=brand_id)
            db.session.add(user_brand)
            db.session.commit()
            return jsonify({'statusCode': 200, 'message': 'user-brand association successfully created'})
        except Exception as e:
            print(e)
            return jsonify({'statusCode': 500, 'message': 'unable to create new user-brand association'})


    def create_user_drink(self, body):
        user = body['username']
        drink = body['drink']
        try:
            user_drink = None
            drink_data = Drink.query.filter_by(name=drink.lower()).first()
            if drink_data is None: # no such drink exists in our database - create
                drink = drink_service.create_drink(drink)
                user_drink = UserDrink(user_name=user.lower(), drink_id=drink.id)
            else: # drink exists in our database
                drink_id = drink_data.id
                user_drink = UserDrink(user_name=user.lower(), drink_id=drink_id)
            db.session.add(user_drink)
            db.session.commit()
            return jsonify({'statusCode': 200, 'message': 'user-drink association successfully created'})
        except Exception as e:
            print(e)
            return jsonify({'statusCode': 500, 'message': 'unable to create new user-drink association'})


    def get_user_bar(self, user):
        """
        Retrieves all the bars a user likes.
        """
        try:
            bar_data = UserBar.query.filter(user_name=user).all()
            print('bar data:', bar_data)
            return bar_data
        except Exception as e:
            print(e)
            return jsonify({'statusCode': 500, 'message': 'unable to fetch user-bar associations'})


    def get_user_drink(self, user):
        """
        Retrieves all the drinks a user likes.
        """
        try:
            drink_data = UserDrink.query.filter(user_name=user).all()
            print('drink data:', drink_data)
            return drink_data
        except Exception as e:
            print(e)
            return jsonify({'statusCode': 500, 'message': 'unable to fetch user-drink associations'})


    def get_user_brand(self, user):
        """
        Retrieves all the brands a user likes.
        """
        try:
            brand_data = UserBrand.query.filter(user_name=user).all()
            print('brand data:', brand_data)
            return brand_data
        except Exception as e:
            print(e)
            return jsonify({'statusCode': 500, 'message': 'unable to fetch user-brand associations'})


    def delete_user_brand(self, body):
        user = body['username']
        uuid = body['uuid']
        try:
            brand_data = Brand.query.filter_by(uuid=uuid).first()
            user_brand = UserBrand.query.filter_by(user=user, brand_id=brand_data.id).first()
            db.session.delete(user_brand)
            db.session.commit()
            return jsonfiy({'statusCode': 200, 'message': 'successfully deleted user-brand association'})
        except Exception as e:
            return jsonify({'statusCode': 500, 'message': 'unable to delete user-brand association'})


    def delete_user_drink(self, body):
        user = body['username']
        uuid = body['uuid']
        try:
            drink_data = Drink.query.filter_by(uuid=uuid).first()
            user_drink = UserDrink.query.filter_by(user=user, drink_id=drink_data.id).first()
            db.session.delete(user_drink)
            db.session.commit()
            return jsonfiy({'statusCode': 200, 'message': 'successfully deleted user-drink association'})
        except Exception as e:
            print(e)
            return jsonify({'statusCode': 500, 'message': 'unable to delete user-drink association'})


    def delete_user_bar(self, body):
        user = body['username']
        uuid = body['uuid']
        try:
            bar_data = Bar.query.filter_by(uuid=uuid).first()
            user_bar = UserBar.query.filter_by(user=user, bar_id=bar_data.id).first()
            db.session.delete(user_bar)
            db.session.commit()
            return jsonfiy({'statusCode': 200, 'message': 'successfully deleted user-bar association'})
        except Exception as e:
            print(e)
            return jsonify({'statusCode': 500, 'message': 'unable to delete user-bar association'})







    
