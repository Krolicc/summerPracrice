from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseCharacterChronology(BaseModel):
    chronology_point_id: int
    character_id: int


class CreateCharacterChronology(BaseCharacterChronology):
    pass


class UpdateCharacterChronology(BaseCharacterChronology):
    pass


class CharacterChronology(IdInt, BaseCharacterChronology):
    pass
