from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, CharacterBodyType


async def get_body_type_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    body_type: CharacterBodyType = await session.scalar(
        select(CharacterBodyType).filter(CharacterBodyType.id == idx)
    )
    return body_type
