from typing import TYPE_CHECKING

from sqlalchemy import SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .chapter import Chapter


class Part(IdIntPKMixin, Base):
    number: Mapped[int] = mapped_column(SMALLINT, unique=True)
    name: Mapped[str] = mapped_column(unique=True)

    chapters: Mapped[list["Chapter"]] = relationship(back_populates="part")
