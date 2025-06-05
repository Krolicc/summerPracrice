from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .image import Image


class Filter(IdIntPKMixin, Base):
    filter: Mapped[str] = mapped_column(unique=True)

    images: Mapped[list["Image"]] = relationship(
        back_populates="filters",
        secondary="image_filter",
    )
