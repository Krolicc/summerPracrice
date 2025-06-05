from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, CharacterStatus


async def get_character_status_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character_status: CharacterStatus = await session.scalar(
        select(CharacterStatus).filter(CharacterStatus.id == idx)
    )
    return character_status
