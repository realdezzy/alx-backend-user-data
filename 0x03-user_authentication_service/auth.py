#!/usr/bin/env python3
""" Authentication Module. """
from bcrypt import gensalt, hashpw, checkpw
from typing import Optional
from uuid import uuid4
from user import User
from sqlalchemy.orm.exc import NoResultFound


from db import DB


def _hash_password(password: str) -> bytes:
    """Return a hash of the password"""
    encoded_password = password.encode(encoding='utf8', errors='strict')
    salt = gensalt()
    hash = hashpw(password=encoded_password, salt=salt)
    return hash


def _generate_uuid() -> str:
    """ Generate a unique and return as string"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Adds a user to the database with validation"""
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError("User {} already exists.".format(email))
        except NoResultFound:
            password_hash = _hash_password(password)

            new_user = self._db.add_user(email, password_hash)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the password is valid"""
        try:
            existing_user = self._db.find_user_by(email=email)
            valid = checkpw(
                password.encode(),
                existing_user.hashed_password)
            if valid:
                return True
            return False

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Create session id for user"""
        id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)

            self._db.update_user(user.id, session_id=id)
            return id
        except NoResultFound:
            return
        except ValueError:
            return

    def get_user_from_session_id(
            self,
            session_id: str) -> Optional[User]:
        """ Get user from session_id. """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            else:
                return
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """ Destroys the session associated with the given user """
        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Creates and returns the reset password token. """
        try:
            user = self._db.find_user_by(email=email)
            u_id = str(_generate_uuid())
            self._db.update_user(user.id, reset_token=u_id)
            return u_id
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update password. """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = str(_hash_password(password))
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)

        except NoResultFound:
            raise ValueError()
