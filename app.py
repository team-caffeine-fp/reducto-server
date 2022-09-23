from flask import Flask, request, jsonify
import os
import subprocess as sp
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
from users import user_schema

load_dotenv()
mongopass = os.getenv('mongopass')
ca = certifi.where()

client = MongoClient(mongopass, tlsCAFile=ca)
db = client.reducto
coll = db.users


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "hello, welcome to reducto server"

@app.route('/users/', methods=['GET'])
def get_users():
    collection = coll.find()
    for user in collection:
        print(user)
    
    return "showing all users"

@app.route('/dashboard/', methods=['GET'])
def dashboard():
    month = datetime.now().month
    print(month)
    return "the month"


# Not finished
@app.route('/login/', methods=['POST'])
def login():
    return "thanks for logging in"

# No auth
@app.route('/register/', methods=['POST'])
def register():
    username = request.form['username']
    bname = request.form['bname']
    user_schema["username"] = username
    user_schema["businessname"] = bname
    coll.insert_one(user_schema)
    return "Thanks for registering"

# Not finished
@app.route('/form/', methods=['PUT'])
def form():
    user = request.form['username']
    co2 = request.form['co2']
    month = datetime.now().month
    category = request.form["category"]
    coll.update_one( { "username": user}, { '$inc': { f"{category}.{month}": int(co2) }})
    return "User updated"


if __name__ == '__main__':
    app.run(debug=True) # pragma: no cover
