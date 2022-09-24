from flask import Flask
import json
import os
from dotenv import load_dotenv
import certifi
from pymongo import MongoClient
from flask import jsonify, request, current_app
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import requests
from app.api import api
import pymongo

load_dotenv()
mongopass = os.getenv('mongopass')
ca = certifi.where()

client = MongoClient(mongopass, tlsCAFile=ca)
db = client.reducto


app = Flask(__name__)


def doc2json(document):
	json = {}
	for k, v in document.items():
		if isinstance(v, ObjectId):
			json[k] = str(v)
		else:
			json[k] = v
	return json

@api.route('/register', methods=['POST'])
@api.route('/users', methods=['POST'])
def create_user():
	data = request.get_json()

	username = data['username']
	password = data['password']
	name = data['name']
	email = data['email']
	image = data['image']

	if db.users.find_one({'username': username}):
		return jsonify({'error': 'This username already exists.'}), 400

	inserted_id = db.users.insert_one({
		'username': username,
		'password': generate_password_hash(password),
		'name': name,
		'email': email,
		'image': image,
	}).inserted_id

	user = db.users.find_one({'_id': inserted_id})

	return jsonify(doc2json(user)), 200


if __name__ == '__main__':
    app.run(debug=True) # pragma: no cover
