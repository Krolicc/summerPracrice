from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseImageFilter(BaseModel):
    image_id: int
    filter_id: int


class CreateImageFilter(BaseImageFilter):
    pass


class UpdateImageFilter(BaseImageFilter):
    pass


class ImageFilter(IdInt, BaseImageFilter):
    pass
