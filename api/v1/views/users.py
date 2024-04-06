#!/usr/bin/python3
"""Handle requests to the api for User"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from os import environ


@app_views.route("/users/",
                 strict_slashes=False)
def return_users():
    """Return JSON object containing list of users in database"""
    from models import storage
    from models.user import User
    return_list = []
    user_dict = storage.all(User)
    for item in user_dict.values():
        return_list.append(item.to_dict())
    return jsonify(return_list)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['GET'])
def return_a_user(user_id):
    """Return user in database corresponding to user_id"""
    from models import storage
    from models.user import User
    users_dict = storage.all(User)
    for item in users_dict.values():
        if item.id == user_id:
            return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_a_user(user_id):
    """Delete a user from the database"""
    from models import storage
    from models.user import User
    users_dict = storage.all(User)
    for item in users_dict.values():
        if item.id == user_id:
            item.delete()
            storage.save()
            return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Create a new user"""
    from models import storage
    from models.user import User
    from werkzeug.exceptions import HTTPException
    try:
        _instance = request.get_json(force=True)
    except Exception:
        abort(400, "Not a JSON")
    if 'email' not in _instance.keys():
        abort(400, "Missing email")
    if 'password' not in _instance.keys():
        abort(400, "Missing password")
    new_user = User(**_instance)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """Update a user's value in the database"""
    from models import storage
    from models.user import User
    users_dict = storage.all(User)
    for item in users_dict.values():
        if item.id == user_id:
            break
    else:
        abort(404)
    try:
        instance_upd = request.get_json(force=True)
    except Exception:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "created_at", "email", "updated_at"]
    for item in users_dict.values():
        if item.id == user_id:
            for keyy in instance_upd.keys():
                if keyy not in ignored_keys:
                    setattr(item, keyy, instance_upd[keyy])
            item.save()
            break
    return (item.to_dict(), 200)
