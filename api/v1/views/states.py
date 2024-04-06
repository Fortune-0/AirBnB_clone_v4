#!/usr/bin/python3
"""Handle requests to the api for State"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from os import environ


@app_views.route("/states/",
                 strict_slashes=False)
def return_states():
    """Return JSON object containing list of states in database"""
    from models import storage
    from models.state import State
    return_list = []
    state_dict = storage.all(State)
    for item in state_dict.values():
        return_list.append(item.to_dict())
    return jsonify(return_list)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['GET'])
def return_a_state(state_id):
    """Return state in database corresponding to state_id"""
    from models import storage
    from models.state import State
    states_dict = storage.all(State)
    for item in states_dict.values():
        if item.id == state_id:
            return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_a_state(state_id):
    """Delete a state from the database"""
    from models import storage
    from models.state import State
    states_dict = storage.all(State)
    for item in states_dict.values():
        if item.id == state_id:
            item.delete()
            storage.save()
            return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Create a new state"""
    from models import storage
    from models.state import State
    from werkzeug.exceptions import HTTPException
    try:
        _instance = request.get_json(force=True)
    except Exception:
        abort(400, "Not a JSON")
    if 'name' not in _instance.keys():
        abort(400, "Missing name")
    new_state = State(**_instance)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """Update a state's value in the database"""
    from models import storage
    from models.state import State
    states_dict = storage.all(State)
    for item in states_dict.values():
        if item.id == state_id:
            break
    else:
        abort(404)
    try:
        instance_upd = request.get_json(force=True)
    except Exception:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "created_at", "updated_at"]
    for item in states_dict.values():
        if item.id == state_id:
            for keyy in instance_upd.keys():
                if keyy not in ignored_keys:
                    setattr(item, keyy, instance_upd[keyy])
            item.save()
            break
    return (item.to_dict(), 200)
