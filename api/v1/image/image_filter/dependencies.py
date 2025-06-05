from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.models.associate import image_filter


async def get_image_filter_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    image_filter_model: image_filter = await session.scalar(
        select(image_filter).filter(image_filter.id == idx)
    )
    return image_filter_model
