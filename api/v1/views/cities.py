#!/usr/bin/python3
"""Module for cities object"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """list all cities"""

    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """select city by id"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """delete city by id"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create city"""

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


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """update city by id"""

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
    storage.save()
    return make_response(jsonify(old.to_dict()), 200)
