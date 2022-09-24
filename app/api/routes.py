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


def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		user_id = kwargs['user_id']
		auth = request.headers.get('Authorization')

		try:
			token = auth.split(' ')[1]
			payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
			assert user_id == payload['_id']
		except:
			return jsonify({'error': 'Invalid credentials.'}), 400


		return f(*args, **kwargs)

	return wrapper


@api.route('/auth/login', methods=['POST'])
def auth_login():
	data = request.get_json()

	username = data['username']
	password = data['password']

	user = db.users.find_one({'username': username})

	if not user:
		return {'error': 'Username does not exist.'}, 400

	if check_password_hash(user['password'], password):
		token = jwt.encode({
			'_id': str(user['_id'])
		}, current_app.config.get('SECRET_KEY'))

		return jsonify({'token': token, '_id': str(user['_id'])}), 200

	return {'error': 'Password incorrect.'}, 400


@api.route('/auth/logout', methods=['POST'])
def auth_logout():
	return jsonify({'logout': True}), 200


@api.route('/users', methods=['GET'])
def read_user_all():
	users = [
		doc2json(user)
		for user
		in db.users.find()
	]

	return jsonify(users)


@api.route('/users', methods=['DELETE'])
def delete_user_all():
	db.users.delete_many({})

	return 'deleted'


@login_required
@api.route('/users/<user_id>', methods=['GET'])
def read_user(user_id):

	user = doc2json(db.users.find_one({
		'_id': ObjectId(user_id)
	}))

	del user['password']

	return jsonify(user), 200


@api.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
	data = request.get_json()

	username = data['username']
	password = data['password']
	name = data['name']
	email = data['email']
	image = data['image']

	user = db.users.find_one({'username': username})
	if user and str(user['_id']) != user_id:
		return jsonify({'error': 'This username already exists.'}), 400

	upserted_id = db.users.update_one({
		'_id': ObjectId(user_id)
	}, {'$set': {
		'username': username,
		'password': generate_password_hash(password),
		'name': name,
		'email': email,
		'image': image,
	}}).upserted_id

	user = db.users.find_one({'_id': ObjectId(user_id)})

	return jsonify(doc2json(user)), 200


@api.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
	count = db.users.delete_one({
		'_id': ObjectId(user_id)
	}).deleted_count

	if count == 0:
		return jsonify({'error': 'No emissions to delete.'}), 400

	return jsonify(), 200

if __name__ == '__main__':
    app.run(debug=True) # pragma: no cover
