#!/usr/bin/env python3
""" Session authenticated view"""
from flask import jsonify, abort
from api.v1.views import app_views

@app_views.route('/auth_session/login/', methods=['POST'], slashes=False)
def login(request):