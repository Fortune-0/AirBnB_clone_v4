#!/usr/bin/python3
"""Handle requests to the api for Place"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from os import environ


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def return_places(city_id):
    """Return city in database corresponding to city_id"""
    from models import storage
    from models.city import City
    from models.place import Place
    cities_dict = storage.all(City)
    places_dict = storage.all(Place)
    for item in cities_dict.values():
        if item.id == city_id:
            parent_city = item.to_dict()
            break
    else:
        abort(404)
    places_list = []
    for item in places_dict.values():
        if item.city_id == city_id:
            places_list.append(item.to_dict())
    return (jsonify(places_list))


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
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


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
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


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """Create a new place"""
    from models import storage
    from models.place import Place
    from models.city import City
    cities_dict = storage.all(City)
    for item in cities_dict.values():
        if item.id == city_id:
            break
    else:
        abort(404)
    from werkzeug.exceptions import HTTPException
    try:
        _instance = request.get_json(force=True)
    except Exception:
        return ("Not a JSON", 400)
    _instance.update({'city_id': city_id})
    if 'user_id' not in _instance.keys():
        abort(400, "Missing user_id")
    from models.user import User
    user_dict = storage.all(User)
    for item in user_dict.values():
        if item.id == _instance['user_id']:
            break
    else:
        abort(404)
    if 'name' not in _instance.keys():
        abort(400, "Missing name")
    new_place = Place(**_instance)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """Update a place's value in the database"""
    from models import storage
    from models.place import Place
    places_dict = storage.all(Place)
    for item in places_dict.values():
        if item.id == place_id:
            break
    else:
        abort(404)
    try:
        instance_upd = request.get_json(force=True)
    except Exception:
        return ("Not a JSON", 400)
    ignored_keys = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for item in places_dict.values():
        if item.id == place_id:
            for keyy in instance_upd.keys():
                if keyy not in ignored_keys:
                    setattr(item, keyy, instance_upd[keyy])
            item.save()
            break
    return (item.to_dict(), 200)
