#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Find user by keyword arguments"""
        session = self._session
        data = session.query(User).filter_by(**kwargs)

        first_row = data.first()

        if first_row is None:
            raise NoResultFound()

        return first_row

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update user"""
        try:
            user = self.find_user_by(id=user_id)
            if not user:
                return

            valid_attributes = [
                column.name for column in User.__table__.columns]
            for key, value in kwargs.items():
                if key in valid_attributes:
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")
            self.__session.commit()
        except NoResultFound:
            return
