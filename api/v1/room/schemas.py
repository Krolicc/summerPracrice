from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseRoom(BaseModel):
    name: str
    algorithm: str


class CreateRoom(BaseRoom):
    pass


class UpdateRoom(BaseRoom):
    creator_id: int
    interlocutor_id: int | None


class Room(IdInt, BaseRoom):
    creator_id: int
    interlocutor_id: int | None
