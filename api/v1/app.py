#!/usr/bin/python3
"""Define application as instance of Flask"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import environ

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exception=None):
    """Destroy current session at the end of request"""
    storage.close()


@app.errorhandler(404)
def error_handler(err):
    """Handle the 404 error by returning JSON response"""
    error_dict = {"error": "Not found"}
    return make_response(jsonify(error_dict), 404)


if __name__ == "__main__":
    app.run(host=environ.get('HBNB_API_HOST', '0.0.0.0'),
            port=environ.get('HBNB_API_PORT', 5000), threaded=True)
