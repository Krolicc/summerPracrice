from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from ..mixins import IdIntPKMixin

if TYPE_CHECKING:
    from .user import User
    from .image import Image
    from .chapter import Chapter
    from .request import Request


class Profile(IdIntPKMixin, Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        index=True,
    )

    dh_public_key: Mapped[Optional[str]] = mapped_column(
        String(512), nullable=True, default=None
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    # chapters: Mapped[list["Chapter"]] = relationship(
    #     secondary="profile_chapter",
    #     back_populates="profiles",
    # )
    images: Mapped["Image"] = relationship(back_populates="profile")
    requests: Mapped["Request"] = relationship(back_populates="profile")
