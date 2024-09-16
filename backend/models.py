# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

import database

class User(database.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Item(database.Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

class User_Item(database.Base):
    __tablename__ = 'userItems'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    count = Column(Integer)