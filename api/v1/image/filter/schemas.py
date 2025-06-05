from pydantic import BaseModel, ConfigDict

from api.v1.mixins.id_int import IdInt


class BaseFilter(BaseModel):
    filter: str


class CreateFilter(BaseFilter):
    pass


class UpdateFilter(BaseFilter):
    pass


class Filter(BaseFilter, IdInt):
    model_config = ConfigDict(from_attributes=True)
