from flask import Flask, request
from pymongo import MongoClient
from mongopass import mongopass

client = MongoClient(mongopass)
db = client.reducto
coll = db.users


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "hello, welcome to reducto server"

@app.route('/dashboard/', methods=['GET'])
def dashboard():
    return "I don't think we actually need this"

# Not finished
@app.route('/login/', methods=['POST'])
def login():
    return "thanks for logging in"

# Not finished
@app.route('/register/', methods=['POST'])
def register():
    return "Thanks for registering"

# Not finished
@app.route('/form/', methods=['POST'])
def form():
    return "Thanks for letting us know your carbon footprint"


if __name__ == '__main__':
    app.run(debug=True)
