#!/usr/bin/python3
"""This module contains the states view for the API"""


from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def all_states():
    """get the list of all State objects"""
    state_list = []
    for state in storage.all(State).values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>',
                 methods=["GET"], strict_slashes=False)
def state_object(state_id):
    """get a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """delete an object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=["POST"],
                 strict_slashes=False)
def create_state():
    """create a new state object"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        return abort(400, {"Not a JSON"})
    if 'name' not in request_data.keys():
        return abort(400, {"Missing name"})
    new_obj = State(name=request_data['name'])
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """update a state object"""
    request_data = request.get_json()
    if request_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    state_update = storage.get(State, state_id)
    if state_update is None:
        return abort(404)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_update, key, value)
    state_update.save()
    return make_response(jsonify(state_update.to_dict()), 200)
