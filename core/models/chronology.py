from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .chapter import Chapter
    from .date import Date
    from .character import Character


class Chronology(IdIntPKMixin, Base):
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"), nullable=True)
    date_id: Mapped[int] = mapped_column(ForeignKey("date.id"))
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)

    chapters: Mapped["Chapter"] = relationship(back_populates="chronology_points")
    dates: Mapped["Date"] = relationship(back_populates="chronology_points")

    characters: Mapped[list["Character"]] = relationship(
        secondary="character_chronology",
        back_populates="chronology_points",
    )
