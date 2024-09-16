# schemas.py
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float

class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(UserCreate):
    hashed_password: str

class ItemCreate(BaseModel):
    name: str
    price: float

class UserItemCreate(BaseModel):
    user_id: int
    item_id: int
    count: int