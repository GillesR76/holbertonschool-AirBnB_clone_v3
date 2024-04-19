#!/usr/bin/python3
"""This module contains the users view for the API"""


from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/users',
                 methods=["GET"], strict_slashes=False)
def all_users():
    """get the list of all users"""
    users = storage.get(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 methods=["GET"], strict_slashes=False)
def user_object(user_id):
    """get an user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """delete a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=["POST"],
                 strict_slashes=False)
def create_user():
    """create a new user object"""
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'email' not in request_data:
        abort(400, 'Missing email')
    if 'password' not in request_data:
        abort(400, 'Missing password')
    new_user = User(**request_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update a user object"""
    user_update = storage.get(User, user_id)
    if user_update is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_update, key, value)
    user_update.save()
    return jsonify(user_update.to_dict()), 200