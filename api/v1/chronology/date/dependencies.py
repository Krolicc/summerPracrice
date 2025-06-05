from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Date


async def get_date_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    date: Date = await session.scalar(select(Date).filter(Date.id == idx))
    return date
