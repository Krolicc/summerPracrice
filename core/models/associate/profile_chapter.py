from typing import TYPE_CHECKING

from sqlalchemy import SMALLINT, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import IdIntPKMixin
from core.models import Base

if TYPE_CHECKING:
    from core.models.chapter import Chapter
    from core.models.profile import Profile


class ProfileChapter(IdIntPKMixin, Base):
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))

    is_favorite: Mapped[bool] = mapped_column(
        default=False,
        server_default="False",
    )
    is_read: Mapped[bool] = mapped_column(
        default=False,
        server_default="False",
    )
    is_like: Mapped[bool] = mapped_column(nullable=True)

    # chapters: Mapped["Chapter"] = relationship(back_populates="profiles")
    # profiles: Mapped["Profile"] = relationship(back_populates="chapters")

    __table_args__ = (
        UniqueConstraint(
            "profile_id", "chapter_id", name="uq_profile_chapter_profile_id_chapter_id"
        ),
    )
