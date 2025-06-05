from pydantic import BaseModel, ConfigDict

from api.v1.mixins.id_int import IdInt


class BaseCharacterStatus(BaseModel):
    status: str


class CreateCharacterStatus(BaseCharacterStatus):
    pass


class UpdateCharacterStatus(BaseCharacterStatus):
    pass


class CharacterStatus(BaseCharacterStatus, IdInt):
    pass

    model_config = ConfigDict(from_attributes=True)
