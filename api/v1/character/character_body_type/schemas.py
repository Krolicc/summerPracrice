from pydantic import BaseModel, ConfigDict

from api.v1.mixins.id_int import IdInt


class BaseBodyType(BaseModel):
    type: str


class CreateBodyType(BaseBodyType):
    pass


class UpdateBodyType(BaseBodyType):
    pass


class BodyType(BaseBodyType, IdInt):
    model_config = ConfigDict(from_attributes=True)
