from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseDate(BaseModel):
    day: int
    month: int
    year: int


class CreateDate(BaseDate):
    pass


class UpdateDate(BaseDate):
    pass


class Date(BaseDate, IdInt):
    # chronology_points: list[BaseChronologyPoint]
    pass
