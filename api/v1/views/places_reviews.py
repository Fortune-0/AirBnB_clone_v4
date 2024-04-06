#!/usr/bin/python3
"""Handle requests to the api for Review"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from os import environ


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def return_reviews(place_id):
    """Return place in database corresponding to place_id"""
    from models import storage
    from models.place import Place
    from models.review import Review
    places_dict = storage.all(Place)
    reviews_dict = storage.all(Review)
    for item in places_dict.values():
        if item.id == place_id:
            parent_place = item.to_dict()
            break
    else:
        abort(404)
    reviews_list = []
    for item in reviews_dict.values():
        if item.place_id == place_id:
            reviews_list.append(item.to_dict())
    return (jsonify(reviews_list))


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET'])
def return_a_review(review_id):
    """Return review in database corresponding to review_id"""
    from models import storage
    from models.review import Review
    reviews_dict = storage.all(Review)
    for item in reviews_dict.values():
        if item.id == review_id:
            return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_a_review(review_id):
    """Delete a review from the database"""
    from models import storage
    from models.review import Review
    reviews_dict = storage.all(Review)
    for item in reviews_dict.values():
        if item.id == review_id:
            item.delete()
            storage.save()
            return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """Create a new review"""
    from models import storage
    from models.review import Review
    from models.place import Place
    places_dict = storage.all(Place)
    for item in places_dict.values():
        if item.id == place_id:
            break
    else:
        abort(404)
    from werkzeug.exceptions import HTTPException
    try:
        _instance = request.get_json(force=True)
    except Exception:
        return ("Not a JSON", 400)
    _instance.update({'place_id': place_id})
    if 'user_id' not in _instance.keys():
        abort(400, "Missing user_id")
    from models.user import User
    user_dict = storage.all(User)
    for item in user_dict.values():
        if item.id == _instance['user_id']:
            break
    else:
        abort(404)
    if 'text' not in _instance.keys():
        abort(400, "Missing text")
    new_review = Review(**_instance)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Update a review's value in the database"""
    from models import storage
    from models.review import Review
    reviews_dict = storage.all(Review)
    for item in reviews_dict.values():
        if item.id == review_id:
            break
    else:
        abort(404)
    try:
        instance_upd = request.get_json(force=True)
    except Exception:
        return ("Not a JSON", 400)
    ignored_keys = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for item in reviews_dict.values():
        if item.id == review_id:
            for keyy in instance_upd.keys():
                if keyy not in ignored_keys:
                    setattr(item, keyy, instance_upd[keyy])
            item.save()
            break
    return (item.to_dict(), 200)
