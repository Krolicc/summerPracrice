from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Chapter


async def get_chapter_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    chapter: Chapter = await session.scalar(select(Chapter).filter(Chapter.id == idx))
    return chapter
