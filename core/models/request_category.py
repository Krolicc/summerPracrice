from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .request import Request


class RequestCategory(IdIntPKMixin, Base):
    category: Mapped[str] = mapped_column(unique=True)

    requests: Mapped[list["Request"]] = relationship(back_populates="category")
