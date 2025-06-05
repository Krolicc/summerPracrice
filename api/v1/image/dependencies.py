from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Image


async def get_image_by_id(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    image_model: Image = await session.scalar(select(Image).filter(Image.id == idx))
    return image_model
