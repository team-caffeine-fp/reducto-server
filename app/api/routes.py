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
from datetime import datetime, timedelta

load_dotenv()
mongopass = os.getenv('mongopass')
ca = certifi.where()

client = MongoClient(mongopass, tlsCAFile=ca)
db = client.reducto


app = Flask(__name__)

# Convert _id field to string
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

	try:
		username = data['username']
		password = data['password']
		businessname = data['businessname']
		email = data['email']
	except:
		return jsonify({'error': 'Missing fields.'}), 400

	if db.users.find_one({'username': username}):
		return jsonify({'error': 'Username already exists.'}), 400

	inserted_id = db.users.insert_one({
		'username': username,
		'password': generate_password_hash(password),
		'businessname': businessname,
		'email': email,
		'token': ''
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
			user = db.users.find_one({'_id': ObjectId(user_id)})

			assert user
			assert user_id == payload['_id']
			assert user['token'] == token
		except:
			return jsonify({'error': 'Invalid credentials.'}), 401

		return f(*args, **kwargs)

	return wrapper


@api.route('/auth/login', methods=['POST'])
def auth_login():
	data = request.get_json()

	try:
		username = data['username']
		password = data['password']
	except:
		return jsonify({'error': 'Missing fields.'}), 400

	user = db.users.find_one({'username': username})

	if not user:
		return jsonify({'error': 'Username does not exist.'}), 400

	if check_password_hash(user['password'], password):
		token = jwt.encode({
			'_id': str(user['_id']),
			'exp': datetime.now() + timedelta(hours=1)
		}, current_app.config.get('SECRET_KEY'))

		db.users.update_one({'_id': user['_id']}, {'$set': {
			'token': token
		}})

		return jsonify({'token': token, '_id': str(user['_id'])}), 200

	return jsonify({'error': 'Password is incorrect.'}), 400


@api.route('/auth/logout', methods=['POST'])
def auth_logout():
	auth = request.headers.get('Authorization')

	try:
		token = auth.split(' ')[1]
		payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
		user = db.users.find_one({'_id': ObjectId(payload['_id'])})

		assert user
		assert user['token'] == token

		db.users.update_one({'_id': ObjectId(payload['_id'])}, {'$set': {
			'token': ''
		}})
	except:
		return jsonify({'error': 'Invalid credentials.'}), 401

	return jsonify(), 200


@api.route('/users/<user_id>', methods=['GET'])
@login_required
def read_user(user_id):
	try:
		user = doc2json(db.users.find_one({
			'_id': ObjectId(user_id)
		}))
		assert user
	
	except: 
		return jsonify({'error': 'User not found.'}), 404

	del user['password']

	return jsonify(user), 200


@api.route('/users/<user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
	data = request.get_json()

	if 'password' in data:
		data['password'] = generate_password_hash(data['password'])

	if 'username' in data:
		user = db.users.find_one({'username': data['username']})
		if user and str(user['_id']) != user_id:
			return jsonify({'error': 'Username already exists.'}), 400

	try:
		count = db.users.update_one({
			'_id': ObjectId(user_id)
		}, {'$set': data}).matched_count
		assert count != 0
	except: 
		return jsonify({'error': 'User not found.'}), 404 

	user = db.users.find_one({'_id': ObjectId(user_id)})

	return jsonify(doc2json(user)), 200


@api.route('/users/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
	try:
		count = db.users.delete_one({
			'_id': ObjectId(user_id)
		}).deleted_count

		assert count != 0
	except:
		return jsonify({'error': 'User not found.'}), 404

	return jsonify(), 200


@api.route('/users/<user_id>/emissions', methods=['GET'])
@login_required
def read_emission_all(user_id):
	emissions = [
		doc2json(emission)
		for emission
		in db.emissions.find({ 'user_id': ObjectId(user_id)})
	]

	return jsonify(emissions), 200



@api.route('/users/<user_id>/emissions', methods=['POST'])
@login_required
def create_emission(user_id):

	data = request.get_json()

	inserted_id = db.emissions.insert_one({
		'user_id': ObjectId(user_id),
		'category': data['category'],
		'timestamp': data['timestamp'],
		'co2e': data['co2e'] 
	}).inserted_id

	emission = db.emissions.find_one({'_id': inserted_id})

	return jsonify(doc2json(emission)), 200





@api.route('/users/<user_id>/emissions/<emission_id>', methods=['GET'])
@login_required
def read_emission(user_id, emission_id):
	try:
		emission = db.emissions.find_one({
			'_id': ObjectId(emission_id),
			'user_id': ObjectId(user_id)
		})
		assert emission
	except:
		return jsonify({'error': 'Emission not found.'}), 404

	return jsonify(doc2json(emission)), 200



@api.route('/users/<user_id>/emissions/<emission_id>', methods=['PUT'])
@login_required
def update_emission(user_id, emission_id):
	
	data = request.get_json()

	try:
		count = db.emissions.update_one({
			'_id': ObjectId(emission_id),
			'user_id': ObjectId(user_id)
		}, {'$set': data}).matched_count

		assert count != 0
	except: 
		return jsonify({'error': 'Emission not found.'}), 404 

	emission = db.emissions.find_one({'_id': ObjectId(emission_id)})

	return jsonify(doc2json(emission)), 200



@api.route('/users/<user_id>/emissions/<emission_id>', methods=['DELETE'])
@login_required
def delete_emission(user_id, emission_id):
	try:
		count = db.emissions.delete_one({
			'_id': ObjectId(emission_id),
			'user_id': ObjectId(user_id)
		}).deleted_count

		assert count != 0
	except:
		return jsonify({'error': 'Emission not found.'}), 404

	return jsonify(), 200


if __name__ == '__main__':
    app.run(debug=True) # pragma: no cover
