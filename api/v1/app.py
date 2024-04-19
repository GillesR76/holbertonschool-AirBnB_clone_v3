#!/usr/bin/python3
"""Flask web application"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)

app.register_blueprint(app_views)
"""CORS() is a function provided by the Flask_CORS extension
* app: applies the CORS policy to the entire app instance
of the Flask application
* ressources: dictionary that defines the CORS policy:
    - r'/*': expression that matches all routes in the application
    - 'origins':'0.0.0.0': sub dictionary that specifies the policy
    for the matched routes: the application will accept
    cross-origin requests from host 0.0.0.0
The whole line allows cross-origin requests from 0.0.0.0
to all routes in the Flask application.
"""
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(e):
    """return a json formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def remove_session(exception):
    """Closes the database session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
