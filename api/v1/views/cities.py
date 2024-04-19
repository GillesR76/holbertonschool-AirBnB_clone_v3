#!/usr/bin/python3
"""This module contains the cities view for the API"""


from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """get the list of cities of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>',
                 methods=["GET"], strict_slashes=False)
def city_object(city_id):
    """get a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """create a new city object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    new_city = City(name=request_data['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """update a state object"""
    city_update = storage.get(City, city_id)
    if city_update is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_update, key, value)
    city_update.save()
    return make_response(jsonify(city_update.to_dict()), 200)
