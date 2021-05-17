from flask import request, jsonify
from src.app import db
# from src.models.post import Post
from src.models.bar import Bar
from src.models.brand import Brand
from src.models.drink import Drink
from src.models.user import User
from src.models.user_bar import UserBar
from src.models.user_brand import UserBrand
from src.models.user_drink import UserDrink
from src.models.location import Location
from src.models.neighborhood import Neighborhood
from src.service.bar_service import BarService as bar_service
from src.service.neighborhood_service import NeighborhoodService as neighborhood_service
from src.service.drink_service import DrinkService as drink_service
from src.service.brand_service import BrandService as brand_service
from sqlalchemy import func
import logging

class UserService():


    def create_user(self, body):
        try:
            pic_link = None
            bio = None
            username = body['username']
            email = body['email']
            firstname = body['firstName']
            lastname = body['lastName']
            fullname = body['fullName']
            if (body['picLink']):
                pic_link = body['picLink']
            user = User(user_name=username, email=email, first_name=firstname, last_name=lastname, prof_pic=pic_link, full_name=fullname)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'user successfully created'}), 200
        except Exception as e:
            print(e)  
            logging.error(e)  
            return jsonify({'message': 'unable to create user'}), 500
    
    def update_user(self, body, username):
        try:
            user = User.query.filter_by(user_name=username).first()
            if (body['email']):
               user.email = body['email']
            if (body['firstName']):
                user.first_name = body['firstName']
            if (body['lastName']):
                user.last_name = body['lastName']
            if (body['fullName']):
                user.full_name = body['fullName'] 
            if (body['firstName'] and body['lastName'] and not body['fullName']):
                user.full_name = f"{body['firstName']} {body['lastName']}"
            if (body['picLink']):
                user.link_to_prof_pic = body['picLink']
            if (body['bio']):
                user.bio = body['bio']
            db.session.commit()
            return jsonify({'message': 'user successfully updated'}), 200
        except Exception as e:
            print('exception: ', e)
            return jsonify({'message': 'unable to update user'}), 500
    
    def get_user_by_username(self, username):
        try:
            user = User.query.filter_by(user_name=username).first()
            if user is not None:
                num_bars = db.session.query(db.func.count(UserBar.bar_id)).filter_by(user_name=username).scalar()
                num_brands = db.session.query(db.func.count(UserBrand.brand_id)).filter_by(user_name=username).scalar()
                num_drinks = db.session.query(db.func.count(UserDrink.drink_id)).filter_by(user_name=username).scalar()
            else:
                return jsonify({'message': 'No user exists by that username'}), 200
            return jsonify({'username': user.user_name, 'firstName': user.first_name, 
            'lastName': user.last_name, 'fullName': user.full_name, 'email': user.email, 'picLink': user.link_to_prof_pic, 'bio': user.bio,
            'numBars': num_bars, 'numBrands': num_brands, 'numDrinks': num_drinks})
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to grab post'}), 500
    
    def delete_user(self, username):
        try:
            user = User.query.filter_by(user_name=username).first()
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'user successfully deleted'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to delete user'}), 500



    def create_user_bar(self, body):
        user = body['username']
        bar = body['bar']
        try:
            user_bar = None
            nbhood_data = None
            location_data = Location.query.filter_by(location=body['location']).first()
            if 'neighborhood' in body:
                nbhood_data = Neighborhood.query.filter_by(neighborhood=body['neighborhood'].lower()).first()
                bar_data = Bar.query.filter_by(name=bar.lower(), location_id=location_data.id, neighborhood_id=nbhood_data.id).first()
            else:
                bar_data = Bar.query.filter_by(name=bar.lower(), location_id=location_data.id).first()
            if bar_data is None: # no such bar exists in our database - create
                if 'neighborhood' in body: # neighborhood specified
                    if nbhood_data is not None: # neighborhood exists - create bar with it
                        bar_data = bar_service().create_bar(bar_name=bar.lower(), location_id=location_data.id, neighborhood_id=nbhood_data.id)
                    else: # neighborhood does not exist - create it and then create bar
                        nbhood_data = neighborhood_service().create_nbhood(location_id=location_data.id, neighborhood=body['neighborhood'])
                        bar_data = bar_service().create_bar(bar_name=bar, location_id=location_data.id, neighborhood_id=nbhood_data.id)
                else: # no neighborhood specified - create bar without neighborhood
                    bar_data = bar_service().create_bar(bar_name=bar, location_id=location_data.id)
                bar_id = bar_data.id
                user_bar = UserBar(user_name=user, bar_id=bar_id)
            else: # bar exists in our database
                bar_id = bar_data.id
                user_bar = UserBar(user_name=user, bar_id=bar_id)
            db.session.add(user_bar)
            db.session.commit()
            return jsonify({'message': 'user-bar association successfully created'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to create new user-bar association'}), 500


    def create_user_brand(self, body):
        user = body['username']
        brand = body['brand']
        try:
            type_brand = body['type']
            user_brand = None
            brand_data = Brand.query.filter_by(name=brand.lower()).first()
            if brand_data is None: # no such brand exists in our database - create
                brand = brand_service().create_brand(brand, type_brand)
                user_brand = UserBrand(user_name=user, brand_id=brand.id)
            else: # brand exists in our database
                brand_id = brand_data.id
                user_brand = UserBrand(user_name=user, brand_id=brand_id)
            db.session.add(user_brand)
            db.session.commit()
            return jsonify({'message': 'user-brand association successfully created'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to create new user-brand association'}), 500


    def create_user_drink(self, body):
        user = body['username']
        drink = body['drink']
        try:
            user_drink = None
            drink_data = Drink.query.filter_by(name=drink.lower()).first()
            if drink_data is None: # no such drink exists in our database - create
                drink = drink_service().create_drink(drink)
                user_drink = UserDrink(user_name=user, drink_id=drink.id)
            else: # drink exists in our database
                drink_id = drink_data.id
                user_drink = UserDrink(user_name=user, drink_id=drink_id)
            db.session.add(user_drink)
            db.session.commit()
            return jsonify({'message': 'user-drink association successfully created'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to create new user-drink association'}), 500


    def get_user_bar(self, user, page):
        """
        Retrieves all the bars a user likes.
        """
        try:
            bar_data = UserBar.query.filter_by(user_name=user).paginate(page=page, per_page=5)
            num_bars = db.session.query(db.func.count(UserBar.bar_id)).filter_by(user_name=user).scalar()
            bars = []
            for item in bar_data.items:
                bar = Bar.query.filter_by(id=item.bar_id).join(Location, Bar.location_id == Location.id).outerjoin(Neighborhood, Bar.neighborhood_id == Neighborhood.id).first()
                temp = {'user': item.user_name, 'barName': bar.name, 'location': bar.location.location, 'neighborhood': ('' if bar.neighborhood is None else bar.neighborhood.neighborhood), 'uuid': bar.uuid}
                bars.append(temp)
            response = {'totalCount': num_bars, 'bars': bars}
            return jsonify(response)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to fetch user-bar associations'}), 500


    def get_user_drink(self, user, page):
        """
        Retrieves all the drinks a user likes.
        """
        try:
            drink_data = UserDrink.query.filter_by(user_name=user).paginate(page=page, per_page=5)
            num_drinks = db.session.query(db.func.count(UserDrink.drink_id)).filter_by(user_name=user).scalar()
            drinks = []
            for item in drink_data.items:
                drink_name = Drink.query.filter_by(id=item.drink_id).first()
                temp = {'user': item.user_name, 'drinkName': drink_name.name, 'uuid': drink_name.uuid}
                drinks.append(temp)
            response = {'totalCount': num_drinks, 'drinks': drinks}
            return jsonify(response)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to fetch user-drink associations'}), 500


    def get_user_brand(self, user, page):
        """
        Retrieves all the brands a user likes.
        """
        try:
            brand_data = UserBrand.query.filter_by(user_name=user).paginate(page=page, per_page=5)
            num_brands = db.session.query(db.func.count(UserBrand.brand_id)).filter_by(user_name=user).scalar()
            brands = []
            for item in brand_data.items:
                brand_name = Brand.query.filter_by(id=item.brand_id).first()
                temp = {'user': item.user_name, 'brandName': brand_name.name, 'uuid': brand_name.uuid, 'type': brand_name.type}
                brands.append(temp)
            response = {'totalCount': num_brands, 'brands': brands}
            return jsonify(response)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to fetch user-brand associations'}), 500


    def delete_user_brand(self, body):
        user = body['username']
        uuid = body['uuid']
        try:
            brand_data = Brand.query.filter_by(uuid=uuid).first()
            user_brand = UserBrand.query.filter_by(user_name=user, brand_id=brand_data.id).first()
            db.session.delete(user_brand)
            db.session.commit()
            return jsonify({'message': 'successfully deleted user-brand association'}), 200
        except Exception as e:
            return jsonify({'message': 'unable to delete user-brand association'}), 500


    def delete_user_drink(self, body):
        user = body['username']
        uuid = body['uuid']
        try:
            drink_data = Drink.query.filter_by(uuid=uuid).first()
            user_drink = UserDrink.query.filter_by(user_name=user, drink_id=drink_data.id).first()
            db.session.delete(user_drink)
            db.session.commit()
            return jsonify({'message': 'successfully deleted user-drink association'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to delete user-drink association'}), 500


    def delete_user_bar(self, body): # works
        user = body['username']
        uuid = body['uuid']
        try:
            bar_data = Bar.query.filter_by(uuid=uuid).first()
            user_bar = UserBar.query.filter_by(user_name=user, bar_id=bar_data.id).first()
            db.session.delete(user_bar)
            db.session.commit()
            return jsonify({'message': 'successfully deleted user-bar association'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to delete user-bar association'}), 500







    
