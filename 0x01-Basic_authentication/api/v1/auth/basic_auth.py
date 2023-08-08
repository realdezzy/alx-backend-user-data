#!/usr/bin/env python3
"""BasicAuth Module"""
from base64 import standard_b64decode
from typing import TypeVar
from models.user import User
from .auth import Auth


class BasicAuth(Auth):
    """Basic auth implementation"""
    def __init__(self):
        """Initialize"""
        pass

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extracts the base64 authorization header

        Args:
            authorization_header (str): Authorization header

        Returns:
            str: base64 authorization data
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None
        if (not authorization_header.startswith('Basic ')):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode base64 authorization header

        Args:
            base64_authorization_header (str): Header to decode

        Returns:
            str: Decoded output
        """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded = standard_b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except UnicodeDecodeError:
            return None
        except Exception as e:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user credentials from decoded authorization header"""
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header):
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        userList = User.search({'email': user_email})
        user = None
        if len(userList) == 0:
            return None
        for checkUser in userList:
            if checkUser.is_valid_password(user_pwd):
                user = checkUser
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request """
        header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(base64_header)
        user_mail, passwd = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(user_mail, passwd)

        return user
