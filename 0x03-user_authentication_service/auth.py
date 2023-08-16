#!/usr/bin/env python3
""" Authentication Module"""
from bcrypt import gensalt, hashpw
from typing import Optional, ByteString
from uuid import uuid4
from user import User
from sqlalchemy.orm.exc import NoResultFound


from db import DB


def _hash_password(password: str) -> bytes:
    """Return a hash of the password"""
    encoded_password: bytes = password.encode()
    salt: bytes = gensalt()
    return hashpw(encoded_password, salt)


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
            valid = bcrypt.checkpw(
                password.encode(),
                existing_user.hashed_password)
            if valid:
                return True
            return False

        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """ Generate a unique and return as string"""
        return str(uuid4())

    def create_session(self, email: str) -> str:
        """ Create session id for user"""
        id = self._generate_uuid()
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
            session_id: str) -> Optional[User | None]:
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
        """ Creates and returns the reset password token """
        try:
            user = self._db.find_user_by_email(email=email)
            if user:
                u_id = self._generate_uuid()
                self._db.update_user(user.id, reset_token=u_id)
                return u_id
        except NoResultFound:
            raise ValueError()
