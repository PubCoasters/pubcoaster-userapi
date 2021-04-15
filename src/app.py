from flask import Flask, request, jsonify
import json
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{Config.credentials['username']}:{Config.credentials['password']}@/{Config.credentials['schema']}?unix_socket=/cloudsql/{Config.credentials['connectionname']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app)

from service.user_service import UserService as user_service


@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    return jsonify({'message': 'test works'})
@app.route('/user/bar', methods=['POST', 'DELETE'])
@cross_origin()
def user_bar():
    if request.method == 'POST':
        return user_service().create_user_bar(request.json)
    else:
        return user_service().delete_user_bar(request.json)


@app.route('/user/drink', methods=['POST', 'DELETE'])
@cross_origin()
def user_drink():
    if request.method == 'POST':
        return user_service().create_user_drink(request.json)
    else:
        return user_service().delete_user_drink(request.json)


@app.route('/user/brand', methods=['POST', 'DELETE'])
@cross_origin()
def user_brand():
    if request.method == 'POST':
        return user_service().create_user_brand(request.json)
    else:
        return user_service().delete_user_brand(request.json)


@app.route('/brand/<string:username>', methods=['GET'])
@cross_origin()
def get_user_brand(username):
    return user_service().get_user_brand(username)


@app.route('/drink/<string:username>', methods=['GET'])
@cross_origin()
def get_user_drink(username):
    return user_service().get_user_drink(username)


@app.route('/bar/<string:username>', methods=['GET'])
@cross_origin()
def get_user_bar(username):
    return user_service().get_user_bar(username)

@app.route('/user/<string:username>', methods=['GET', 'PATCH', 'DELETE'])
@cross_origin()
def user(username):
    if request.method == 'GET':
        return user_service().get_user_by_username(username)
    elif request.method == 'PATCH':
        return user_service().update_user(request.json, username)
    else:
        return user_service().delete_user(username)

@app.route('/user', methods=['POST'])
@cross_origin()
def create_user():
    return user_service().create_user(request.json)
   

# if __name__ == '__main__':
#     app.run()