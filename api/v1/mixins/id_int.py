from pydantic import BaseModel


class IdInt(BaseModel):
    id: int
