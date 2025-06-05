from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .filter import Filter
    from .profile import Profile


class Image(IdIntPKMixin, Base):
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
    created_by_AI: Mapped[bool] = mapped_column(nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="images")

    filters: Mapped[list["Filter"]] = relationship(
        back_populates="images",
        secondary="image_filter",
    )
