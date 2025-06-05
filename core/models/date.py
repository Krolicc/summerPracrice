from typing import TYPE_CHECKING

from sqlalchemy import SMALLINT, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .chronology import Chronology


class Date(IdIntPKMixin, Base):
    day: Mapped[int] = mapped_column(SMALLINT)
    month: Mapped[int] = mapped_column(SMALLINT)
    year: Mapped[int] = mapped_column(SMALLINT)

    chronology_points: Mapped[list["Chronology"]] = relationship(back_populates="dates")

    __table_args__ = (
        UniqueConstraint("day", "month", "year", name="uq_dates_day_month_year"),
    )
