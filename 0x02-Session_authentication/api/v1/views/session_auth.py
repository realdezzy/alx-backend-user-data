#!/usr/bin/env python3
""" Session authenticated view"""
from flask import jsonify, abort, request
from os import getenv
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login/', methods=['POST'], strict_slashes=False)
def login():
    """ Login route"""
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    userList = User.search({'email': email})
    user = None
    if len(userList) == 0:
        return jsonify({ "error": "no user found for this email" }), 404

    for checkUser in userList:
        if checkUser.is_valid_password(password):
            user = checkUser
            break

    if user is None:
        return jsonify({ "error": "wrong password" }), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    cookie_name = getenv('SESSION_NAME')

    response = jsonify(user.to_json())
    response.set_cookie(cookie_name, session_id)

    return response
