from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Chronology


async def get_chronology_point_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Chronology:
    date: Chronology = await session.scalar(
        select(Chronology).filter(Chronology.id == idx)
    )
    return date
