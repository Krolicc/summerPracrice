from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseChapter(BaseModel):
    number: int
    title: str
    description: str
    image: str
    part_id: int


class CreateChapter(BaseChapter):
    pass


class UpdateChapter(BaseChapter):
    pass


class Chapter(IdInt, BaseChapter):
    pass
