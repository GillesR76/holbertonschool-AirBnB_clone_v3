#!/usr/bin/python3
"""This module contains the index view for the API"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def index():
    """new route to display 'status': 'OK'"""
    data = {'status': 'OK'}
    return jsonify(data)


@app_views.route('/stats', strict_slashes=False)
def objects_stats():
    """retrieve the number of each object by type"""
    stats = {"amenities": "Amenity",
             "cities": "City",
             "places": "Place",
             "reviews": "Review",
             "states": "State",
             "users": "User"}
    for key, value in stats.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
