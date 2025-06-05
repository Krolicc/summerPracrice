from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Filter


async def get_filter_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    filter_model: Filter = await session.scalar(select(Filter).filter(Filter.id == idx))
    return filter_model
