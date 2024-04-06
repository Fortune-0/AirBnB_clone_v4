#!/usr/bin/python3
"""New file, purpose yet to be found"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def return_json():
    """Return message in json format"""
    dict = {"status": "OK"}
    return (jsonify(dict))


@app_views.route("/stats")
def return_stats():
    """Return count of class instances in storage"""
    from models import storage
    from models.amenity import Amenity
    from models.state import State
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.user import User
    count_dict = {}
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    for k, v in classes.items():
        count_dict.update({k: storage.count(v)})
    return jsonify(count_dict)
