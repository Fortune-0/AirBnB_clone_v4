#!/usr/bin/python3
"""Handle requests to the api for City"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from os import environ


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def return_cities(state_id):
    """Return state in database corresponding to state_id"""
    from models import storage
    from models.state import State
    from models.city import City
    states_dict = storage.all(State)
    cities_dict = storage.all(City)
    for item in states_dict.values():
        if item.id == state_id:
            parent_state = item.to_dict()
            break
    else:
        abort(404)
    cities_list = []
    for item in cities_dict.values():
        if item.state_id == state_id:
            cities_list.append(item.to_dict())
    return (jsonify(cities_list))


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def return_a_city(city_id):
    """Return city in database corresponding to city_id"""
    from models import storage
    from models.city import City
    cities_dict = storage.all(City)
    for item in cities_dict.values():
        if item.id == city_id:
            return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_a_city(city_id):
    """Delete a city from the database"""
    from models import storage
    from models.city import City
    cities_dict = storage.all(City)
    for item in cities_dict.values():
        if item.id == city_id:
            item.delete()
            storage.save()
            return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """Create a new city"""
    from models import storage
    from models.city import City
    from models.state import State
    states_dict = storage.all(State)
    for item in states_dict.values():
        if item.id == state_id:
            break
    else:
        abort(404)
    from werkzeug.exceptions import HTTPException
    try:
        _instance = request.get_json(force=True)
    except Exception:
        return ("Not a JSON", 400)
    _instance.update({'state_id': state_id})
    if 'name' not in _instance.keys():
        return ("Missing name", 400)
    new_city = City(**_instance)
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Update a city's value in the database"""
    from models import storage
    from models.city import City
    cities_dict = storage.all(City)
    for item in cities_dict.values():
        if item.id == city_id:
            break
    else:
        abort(404)
    try:
        instance_upd = request.get_json(force=True)
    except Exception:
        return ("Not a JSON", 400)
    ignored_keys = ["id", "created_at", "updated_at", "state_id"]
    for item in cities_dict.values():
        if item.id == city_id:
            for keyy in instance_upd.keys():
                if keyy not in ignored_keys:
                    setattr(item, keyy, instance_upd[keyy])
            item.save()
            break
    return (item.to_dict(), 200)
