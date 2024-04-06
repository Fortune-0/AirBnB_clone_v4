#!/usr/bin/python3
"""Handle requests to the api for Amenity"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from os import environ


@app_views.route("/amenities/", methods=['GET'],
                 strict_slashes=False)
def return_amenities():
    """Return JSON object containing list of amenities in database"""
    from models import storage
    from models.amenity import Amenity
    return_list = []
    amenity_dict = storage.all(Amenity)
    for item in amenity_dict.values():
        return_list.append(item.to_dict())
    return jsonify(return_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def return_a_amenity(amenity_id):
    """Return amenity in database corresponding to amenity_id"""
    from models import storage
    from models.amenity import Amenity
    amenities_dict = storage.all(Amenity)
    for item in amenities_dict.values():
        if item.id == amenity_id:
            return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_a_amenity(amenity_id):
    """Delete a amenity from the database"""
    from models import storage
    from models.amenity import Amenity
    amenities_dict = storage.all(Amenity)
    for item in amenities_dict.values():
        if item.id == amenity_id:
            item.delete()
            storage.save()
            return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """Create a new amenity"""
    from models import storage
    from models.amenity import Amenity
    from werkzeug.exceptions import HTTPException
    try:
        _instance = request.get_json(force=True)
    except Exception:
        return ("Not a JSON", 400)
    if 'name' not in _instance.keys():
        return ("Missing name", 400)
    new_amenity = Amenity(**_instance)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Update a amenity's value in the database"""
    from models import storage
    from models.amenity import Amenity
    amenities_dict = storage.all(Amenity)
    for item in amenities_dict.values():
        if item.id == amenity_id:
            break
    else:
        abort(404)
    try:
        instance_upd = request.get_json(force=True)
    except Exception:
        return ("Not a JSON", 400)
    ignored_keys = ["id", "created_at", "updated_at"]
    for item in amenities_dict.values():
        if item.id == amenity_id:
            for keyy in instance_upd.keys():
                if keyy not in ignored_keys:
                    setattr(item, keyy, instance_upd[keyy])
            item.save()
            break
    return (item.to_dict(), 200)
