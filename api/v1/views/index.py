#!/usr/bin/python3
"""This module contains the index view for the API"""

from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/status')
def index():
    """new route to display 'status': 'OK'"""
    data = {'status': 'OK'}
    return jsonify(data)
