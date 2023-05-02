#!/usr/bin/python3
"""
Creates a route status on the object that returns a JSON file
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returns a JSON status message"""
    return jsonify({"status", "OK"})
