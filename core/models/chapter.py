from typing import TYPE_CHECKING

from sqlalchemy import SMALLINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .chronology import Chronology
    from .part import Part
    from .character import Character
    from .profile import Profile


class Chapter(IdIntPKMixin, Base):
    number: Mapped[int] = mapped_column(SMALLINT, unique=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)

    part_id: Mapped[int] = mapped_column(ForeignKey("part.id"))

    chronology_points: Mapped[list["Chronology"]] = relationship(
        back_populates="chapters"
    )
    part: Mapped["Part"] = relationship(back_populates="chapters")

    characters: Mapped[list["Character"]] = relationship(
        secondary="character_chapter",
        back_populates="chapters",
    )

    # profiles: Mapped[list["Profile"]] = relationship(
    #     secondary="profile_chapter",
    #     back_populates="chapters",
    # )
