#!/usr/bin/env python3
"""Authentication Module"""
from flask import request
from re import match
from os import getenv
from typing import List, TypeVar


class Auth:
    """ Auth class: contains all required for authentication"""
    def __init__(self) -> None:
        """Initialize Auth class"""
        pass

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """Checks if a path requires authentication"""

        if (path is None or exclude_paths is None or
                len(exclude_paths) == 0):
            return True

        mod_path = path if match(r'/api/v1/[A-Za-z]*/$', path) \
            else path + '/'
        if mod_path in exclude_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Flask request object"""
        if request is None:
            return None

        if request.headers.get('Authorization'):
            return request.headers.get('Authorization')
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user"""
        return None
    
    def session_cookie(self, request=None):
        """ Retrieve cookie from session"""
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        cookie = request.cookies.get(session_name)

        return cookie
