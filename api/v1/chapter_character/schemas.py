from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseChapterCharacter(BaseModel):
    chapter_id: int
    character_id: int


class CreateChapterCharacter(BaseChapterCharacter):
    pass


class UpdateChapterCharacter(BaseChapterCharacter):
    pass


class ChapterCharacter(IdInt, BaseChapterCharacter):
    pass
