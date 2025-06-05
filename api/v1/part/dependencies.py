from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Part


async def get_part_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    part: Part = await session.scalar(select(Part).filter(Part.id == idx))
    return part
