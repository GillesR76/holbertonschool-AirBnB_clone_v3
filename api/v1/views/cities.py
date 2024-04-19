#!/usr/bin/python3
"""This module contains the cities view for the API"""

from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """get the list of cities of a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>',
                 methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """get a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """create a new city object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    new_city = request.get_json(silent=True)
    if not new_city:
        return abort(400, {"Not a JSON"})
    if "name" not in new_city.keys():
        return abort(400, {"Missing name"})

    new_obj = City(name=new_city['name'], state_id=state_id)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """update a state object"""
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})

    old = storage.get(City, city_id)
    if not old:
        return abort(404)

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in new.items():
        if key not in ignore:
            setattr(old, key, value)
    old.save()
    return make_response(jsonify(old.to_dict()), 200)
