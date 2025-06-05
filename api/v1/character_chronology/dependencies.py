from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, character_chronology


async def get_character_chronology_point_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character_chronology_model: character_chronology = await session.scalar(
        select(character_chronology).filter(character_chronology.id == idx)
    )
    return character_chronology_model
