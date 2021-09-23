from flask import Blueprint, current_app, request, jsonify
from werkzeug.local import LocalProxy
from .models import User
from app import db
import hashlib

accounts = Blueprint('accounts', __name__)
logger = LocalProxy(lambda: current_app.logger)

@accounts.before_request
def before_request_func():
    current_app.logger.name = 'accounts'

@accounts.route('/register', methods=['POST'])
def register():
    db.session.add(
        User(
            username = request.get_json()["username"],
            email = request.get_json()["email"],
            # password = hashlib.md5(request.get_json()["password"].encode())
            password = request.get_json()["password"]
        )
    )
    db.session.commit()
    return 'User created successfully.'


@accounts.route('/update-details/<int:id>', methods=['PATCH'])
def update_details(id=None):

    user = User.query.get(id)
    if "username" in request.get_json():
        user.username = request.get_json()["username"]
    if "email" in request.get_json():
        user.email = request.get_json()["email"]
    db.session.commit()
    return f'User created successfully.{user.username}'


@accounts.route('/delete-user/<int:id>', methods=['DELETE'])
def delete_user(id=None):

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return "User deleted successfully."


@accounts.route('/fetch-user/<int:id>', methods=['GET'])
def fetch_user(id=None):

    user = User.query.get(id)
    
    data = {
        "id": user.id,
        "username" : user.username,
        "email": user.email
    }

    return jsonify(data)