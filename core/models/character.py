from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .character_status import CharacterStatus
    from .character_body_type import CharacterBodyType
    from .chapter import Chapter
    from .chronology import Chronology


class Character(IdIntPKMixin, Base):
    name: Mapped[str]
    age: Mapped[int] = mapped_column(nullable=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    height: Mapped[int] = mapped_column(nullable=True)
    parents: Mapped[str] = mapped_column(nullable=True)
    brief: Mapped[str] = mapped_column(nullable=True)
    favorite_phrase: Mapped[str] = mapped_column(nullable=True)

    body_type_id: Mapped[int] = mapped_column(
        ForeignKey("character_body_type.id"),
        nullable=True,
    )
    status_id: Mapped[int] = mapped_column(
        ForeignKey("character_status.id"),
        nullable=True,
    )

    body_type: Mapped["CharacterBodyType"] = relationship(back_populates="character")
    status: Mapped["CharacterStatus"] = relationship(back_populates="character")

    chapters: Mapped[list["Chapter"]] = relationship(
        back_populates="characters", secondary="character_chapter"
    )

    chronology_points: Mapped[list["Chronology"]] = relationship(
        secondary="character_chronology",
        back_populates="characters",
    )
