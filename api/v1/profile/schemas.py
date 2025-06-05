from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseProfile(BaseModel):
    user_id: int


class CreateProfile(BaseProfile):
    pass


class UpdateProfile(BaseProfile):
    pass


class Profile(IdInt, BaseProfile):
    pass
