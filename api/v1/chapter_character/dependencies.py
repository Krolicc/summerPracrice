from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, character_chapter


async def get_character_chapter_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character_chapter_model: character_chapter = await session.scalar(
        select(character_chapter).filter(character_chapter.id == idx)
    )
    return character_chapter_model
