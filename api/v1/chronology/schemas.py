from pydantic import BaseModel

from api.v1.mixins.id_int import IdInt


class BaseChronologyPoint(BaseModel):
    title: str
    description: str | None

    chapter_id: int
    date_id: int


class CreateChronologyPoint(BaseChronologyPoint):
    pass


class UpdateChronologyPoint(BaseChronologyPoint):
    pass


class ChronologyPoint(BaseChronologyPoint, IdInt):
    pass
