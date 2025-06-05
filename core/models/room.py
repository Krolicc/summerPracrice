from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from ..mixins import IdIntPKMixin


class Room(IdIntPKMixin, Base):
    name: Mapped[str | None]

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id"),
        index=True,
    )

    interlocutor_id: Mapped[int | None] = mapped_column(
        ForeignKey("profile.id"), nullable=True
    )

    algorithm: Mapped[str]
