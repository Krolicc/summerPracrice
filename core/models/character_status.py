from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .character import Character


class CharacterStatus(IdIntPKMixin, Base):
    status: Mapped[str] = mapped_column(unique=True)

    character: Mapped[list["Character"]] = relationship(back_populates="status")
