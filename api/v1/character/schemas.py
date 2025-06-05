from pydantic import BaseModel, ConfigDict, Field, computed_field

from api.v1.character.character_body_type.schemas import BodyType
from api.v1.character.character_status.schemas import CharacterStatus
from api.v1.chronology.schemas import ChronologyPoint
from api.v1.mixins.id_int import IdInt


class BaseCharacter(BaseModel):
    name: str

    age: int | None
    weight: int | None
    height: int | None

    brief: str | None
    favorite_phrase: str | None
    parents: str | None


class CreateCharacter(BaseCharacter):
    pass


class UpdateCharacter(BaseCharacter):
    pass


class CharacterTotal(BaseCharacter, IdInt):
    body_type_id: int | None
    status_id: int | None


class CharacterOne(BaseCharacter, IdInt):
    body_type_model: BodyType | None = Field(exclude=True, alias="body_type")
    status_model: CharacterStatus | None = Field(exclude=True, alias="status")

    @computed_field
    @property
    def body_type(self) -> str | None:
        return self.body_type_model.type if self.body_type_model else None

    @computed_field
    @property
    def status(self) -> str | None:
        return self.status_model.status if self.status_model else None

    chronology_points: list[ChronologyPoint]

    model_config = ConfigDict(from_attributes=True)
