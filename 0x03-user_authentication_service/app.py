#!/usr/bin/env python3
"""Flask Application"""
from flask import (
    Flask,
    abort,
    request,
    redirect,
    jsonify,
    Response,
    make_response)
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ App root route. """
    return jsonify({"message": "Bienvenue"})


@app.route('/users/', methods=['POST'], strict_slashes=False)
def users() -> Response:
    """ Register user """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        if user:
            return jsonify({"email": "{}".format(email),
                            "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 404


@app.route('/profile/', methods=['GET'], strict_slashes=False)
def profile() -> Response:
    """ Profile route """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        return jsonify({"email": "{}".format(user.email)})
    else:
        abort(403)


@app.route('/sessions/', methods=['POST'], strict_slashes=False)
def login() -> Response:
    """ login user"""
    email = request.form.get('email')
    password = request.form.get('password')

    is_valid_user = AUTH.valid_login(email, password)
    if is_valid_user:
        session_id = AUTH.create_session(email)
        resp = make_response()
        resp.set_cookie("session_id", session_id)
        return jsonify(
            {"email": "{}".format(email), "message": "logged in"})
    else:
        abort(401)


@app.route('/sessions/', methods=['DELETE'], strict_slashes=False)
def logout() -> Response:
    """ Logout user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        redirect('/')
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
