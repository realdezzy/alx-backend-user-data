#!/usr/bin/env python3
"""Authentication Module"""
from flask import request
from re import match
from typing import List, TypeVar


class Auth:
    """ Auth class: contains all required for authentication"""

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """Checks if a path requires authentication"""
        if (path == None or exclude_paths == None
            or len(exclude_paths) == 0):
            return True
        mod_path = path if match(r'/api/v1/[A-Za-z]*/$', path) \
                    else path + '/'
        if mod_path in exclude_paths:
            return False
        else:
            return True


    def authorization_header(self, request=None) -> str:
        """Flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user"""
        return None
