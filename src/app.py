from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import os
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sahil23!@localhost/app_localdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app)

from src.service.user_service import UserService as user_service


@app.route('/user/bar', methods=['POST', 'DELETE'])
@cross_origin()
def user_bar():
    print(sys.path)
    if request.method == 'POST':
        return user_service.create_user_bar(request.json)
    else:
        return user_service.delete_user_bar(request.json)


@app.route('/user/drink', methods=['POST', 'DELETE'])
@cross_origin()
def user_drink():
    if request.method == 'POST':
        return user_service.create_user_drink(request.json)
    else:
        return user_service.delete_user_drink(request.json)


@app.route('/brand/<string:username>', methods=['GET'])
@cross_origin()
def get_user_brand(username):
    return user_service.get_user_brand(username)


@app.route('/drink/<string:username>', methods=['GET'])
@cross_origin()
def get_user_drink(username):
    return user_service.get_user_drink(username)


@app.route('/bar/<string:username>', methods=['GET'])
@cross_origin()
def get_user_bar(username):
    return user_service.get_user_bar(username)


if __name__ == '__main__':
    app.run()