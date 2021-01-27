from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import random
import string

from model_mongodb import User


def random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))


app = Flask(__name__)
CORS(app)


@app.route('/users/<user_id>', methods=['GET', 'DELETE'])
def get_user(user_id):
    users = User.find_all(_id=user_id)
    if len(users) == 0:
        return jsonify(success=False, status=404)
    [user] = users

    if request.method == 'GET':
        return user
    elif request.method == 'DELETE':
        user.remove()
        return user


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        return jsonify(list(User.find_all(**request.args)))
    elif request.method == 'POST':
        user = User(request.get_json())
        user.save()
        return make_response(jsonify(user), 201)
    raise Exception("Unsupported method")


@app.route('/')
def hello_world():
    return 'Hello, world!'
