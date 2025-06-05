from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, ProfileChapter


async def get_profile_chapter_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    profile_chapter: ProfileChapter = await session.scalar(
        select(ProfileChapter).filter(ProfileChapter.id == idx)
    )
    return profile_chapter
