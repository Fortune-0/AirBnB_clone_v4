#!/usr/bin/python3
"""Handle requests to the api for Amenity"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from os import environ


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET'])
def retrieve_amenities(place_id):
    """Return place in database corresponding to place_id"""
    from models import storage
    from models.place import Place
    from models.amenity import Amenity
    places_dict = storage.all(Place)
    amenities_dict = storage.all(Amenity)
    for item in places_dict.values():
        if item.id == place_id:
            ams_list = []
            if environ.get('HBNB_TYPE_STORAGE') == 'db':
                am_ref = item.amenities
            else:
                am_ref = item.amenity_ids
            for obj in amenities_dict.values():
                if storage.get(Amenity, obj.id) in am_ref:
                    ams_list.append(obj.to_dict())
            return (jsonify(ams_list))
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_one_amenity(place_id, amenity_id):
    """Unlink an amenity from a place."""
    from models import storage
    from models.place import Place
    from models.amenity import Amenity
    places_dict = storage.all(Place)
    amenities_dict = storage.all(Amenity)
    for item in places_dict.values():
        if item.id == place_id:
            for it in amenities_dict.values():
                if it.id == amenity_id:
                    break
            else:
                abort(404)
            if environ.get('HBNB_TYPE_STORAGE') == 'db':
                if amenity_id not in item.amenities:
                    abort(404)
                else:
                    item.amenities.remove(amenity_id)
                    storage.save()
                    return (jsonify({}), 200)
                    break
            elif environ.get('HBNB_TYPE_STORAGE') != 'db':
                if amenity_id not in item.amenity_ids:
                    abort(404)
                else:
                    item.amenity_ids.remove(amenity_id)
                    storage.save()
                    return (jsonify({}), 200)
                    break
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['POST'])
def add_an_amenity(place_id, amenity_id):
    """Create a new amenity linked to a place"""
    from models import storage
    from models.amenity import Amenity
    from models.place import Place
    places_dict = storage.all(Place)
    for item in places_dict.values():
        if item.id == place_id:
            break
    else:
        abort(404)
    amenities_dict = storage.all(Amenity)
    for item in amenities_dict.values():
        if item.id == amenity_id:
            break
    else:
        abort(404)
    for item in places_dict.values():
        if item.id == place_id:
            if environ.get('HBNB_TYPE_STORAGE') == 'db':
                if amenity_id not in item.amenities:
                    print(item.amenities)
                    exit
                    item.amenities.append(storage.get(Amenity, amenity_id))
                    storage.save()
                    return (jsonify((storage.get(Amenity,
                                                 amenity_id)).to_dict()),
                            201)
                else:
                    return (storage.get(Amenity, amenity_id), 200)
            elif environ.get('HBNB_TYPE_STORAGE') != 'db':
                if amenity_id not in item.amenity_ids:
                    item.amenity_ids.append(storage.get(Amenity, amenity_id))
                    storage.save()
                    return (jsonify((storage.get(Amenity,
                                                 amenity_id)).to_dict()),
                            201)
                else:
                    return (storage.get(Amenity, amenity_id), 200)
