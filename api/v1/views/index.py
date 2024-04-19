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


@app_views.route('/status')
def index():
    """new route to display 'status': 'OK'"""
    data = {'status': 'OK'}
    return jsonify(data)


@app_views.route('/api/v1/stats')
def objects_stats():
    """retrieve the number of each object by type"""
    stats = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(stats)
