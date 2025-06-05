from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.mixins import IdIntPKMixin
from core.models import Base

from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)

from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .profile import Profile


class User(Base, IdIntPKMixin, SQLAlchemyBaseUserTable[UserIdType]):
    profile: Mapped["Profile"] = relationship(back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
