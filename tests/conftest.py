from app import create_app
import pytest
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

@pytest.fixture()
def client():
	app = create_app()

	load_dotenv()
	mongopass = os.getenv('mongopass')
	ca = certifi.where()

	client = MongoClient(mongopass, tlsCAFile=ca)
	client.drop_database('reducto')

	db = client.reducto
	user_id = db.users.insert_one({
		'username': 'edis',
		'password': generate_password_hash('edis'),
		'businessname': 'Edis Emin',
		'email': 'edisemin@example.com',
		'token': ''
	}).inserted_id


	app.config['user_id'] = user_id

	yield app.test_client()

	client.drop_database('reducto')


