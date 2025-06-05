from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BasePart(BaseModel):
    number: int
    name: str


class CreatePart(BasePart):
    pass


class UpdatePart(BasePart):
    pass


class Part(IdInt, BasePart):
    pass
