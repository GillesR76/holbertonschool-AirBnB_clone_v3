#!/usr/bin/python3
"""This module contains the review view for the API"""


from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews',
                 methods=["GET"], strict_slashes=False)
def all_reviews(place_id):
    """get the list of all review object of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_list = []
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>',
                 methods=["GET"], strict_slashes=False)
def review_object(review_id):
    """get a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place(review_id):
    """delete a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create_place(place_id):
    """create a new review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    if 'text' not in request_data:
        abort(400, 'Missing text')
    user = storage.get(User, request_data['user_id'])
    if user is None:
        abort(404)
    new_review = Review(name=request_data['name'], place_id=place_id)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def update_place(review_id):
    """update a review object"""
    review_update = storage.get(Review, review_id)
    if review_update is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review_update, key, value)
    review_update.save()
    return jsonify(review_update.to_dict()), 200
