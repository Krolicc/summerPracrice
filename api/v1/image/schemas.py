from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field

from .filter.schemas import Filter
from api.v1.mixins.id_int import IdInt


class BaseImage(BaseModel):
    profile_id: int
    title: str | None
    description: str | None
    created_at: datetime
    created_by_AI: bool | None


class CreateImage(BaseImage):
    pass


class UpdateImage(BaseImage):
    pass


class Image(BaseImage, IdInt):
    pass


class FilteredImage(BaseImage, IdInt):
    filters_model: list[Filter] = Field(exclude=True, alias="filters")

    @computed_field
    @property
    def filters(self) -> list[str]:
        return list(map(lambda item: item.filter, self.filters_model))

    model_config = ConfigDict(from_attributes=True)
