#!/usr/bin/python3
"""Handle requests to the api for Place"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from os import environ


@app_views.route("/places/",
                 strict_slashes=False)
def return_places():
    """Return JSON object containing list of places in database"""
    from models import storage
    from models.place import Place
    return_list = []
    place_dict = storage.all(Place)
    for item in place_dict.values():
        return_list.append(item.to_dict())
    return jsonify(return_list)


@app_views.route("/places/<place_id>", methods=['GET'])
def return_a_place(place_id):
    """Return place in database corresponding to place_id"""
    from models import storage
    from models.place import Place
    places_dict = storage.all(Place)
    for item in places_dict.values():
        if item.id == place_id:
            return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_a_place(place_id):
    """Delete a place from the database"""
    from models import storage
    from models.place import Place
    places_dict = storage.all(Place)
    for item in places_dict.values():
        if item.id == place_id:
            item.delete()
            storage.save()
            return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/', methods=['POST'])
def create_place():
    """Create a new place"""
    from models import storage
    from models.place import Place
    from models.user import User
    from werkzeug.exceptions import HTTPException
    try:
        _instance = request.get_json(force=True)
    except Exception:
        abort(400, "Not a JSON")
    if 'user_id' not in _instance.keys():
        abort(400, "Missing user_id")
    user_dict = storage.all(User)
    if 'name' not in _instance.keys():
        abort(400, "Missing name")
    for item in users_dict.values():
        if item.user_id == user_id:
            break
    else:
        abort(404)
    new_place = Place(**_instance)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a place's value in the database"""
    from models import storage
    from models.place import Place
    places_dict = storage.all(Place)
    for item in places_dict.values():
        obj_to_u = item
        break
    else:
        abort(404)
    try:
        instance_upd = request.get_json(force=True)
    except Exception:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "created_at", "user_id", "updated_at"]
    for keyy in instance_upd.keys():
        if keyy not in ignored_keys:
            obj_to_u.__dict__[keyy] = instance_upd[keyy]
    return (obj_to_u.to_dict(), 200)
