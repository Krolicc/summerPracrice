from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Character


async def get_character_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character: Character = await session.scalar(
        select(Character).filter(Character.id == idx)
    )
    return character
