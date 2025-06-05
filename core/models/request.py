from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import SMALLINT, UniqueConstraint, ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from .request_category import RequestCategory
    from .profile import Profile


class Request(IdIntPKMixin, Base):
    category_id: Mapped[int] = mapped_column(
        ForeignKey("request_category.id"),
        index=True,
    )
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))

    title: Mapped[str]
    description: Mapped[str]

    date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        default=datetime.now(timezone.utc),
    )

    category: Mapped["RequestCategory"] = relationship(back_populates="requests")
    profile: Mapped["Profile"] = relationship(back_populates="requests")
