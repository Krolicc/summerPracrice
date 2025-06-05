from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseProfileChapter(BaseModel):
    profile_id: int
    chapter_id: int
    is_favorite: bool
    is_like: bool | None
    is_read: bool


class CreateProfileChapter(BaseProfileChapter):
    pass


class UpdateProfileChapter(BaseProfileChapter):
    pass


class ProfileChapter(IdInt, BaseProfileChapter):
    pass
