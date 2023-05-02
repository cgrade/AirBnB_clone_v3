#!/usr/bin/python3
"""
Imports of everything in the package api.v1.views.index
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""Import everthing in package with wildcard"""
if app_views:
    from api.v1.views.index import *
