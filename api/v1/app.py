#!/usr/bin/python3
"""Flask web application"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(exception):
    """Closes the database session after each request"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """return a json formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
