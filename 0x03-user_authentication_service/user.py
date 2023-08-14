#!/usr/bin/env python3
""" User Model Module"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """ User model dataclass"""
    __tablename__ = 'users'

    id: int = Column(Integer,primary_key=True )
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250))
    reset_token: str = Column(String(250))
