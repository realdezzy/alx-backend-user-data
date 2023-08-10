#!/usr/bin/env python3
""" Session Authentication"""
from uuid import uuid4
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a new session id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve the user_id based on the session_id. """
        if session_id is None or not isinstance(session_id, str):
            return None
        
        return self.user_id_by_session_id.get(session_id)
    
    def current_user(self, request=None):
        """ Return the current user"""
        if request is None:
            return None
        cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id(cookie)

        return User.get(user_id)
