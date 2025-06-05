from typing import Annotated, List

from fastapi import APIRouter, Depends, Body
from sqlalchemy import select, Result, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .image_filter.views import router as image_filter_router
from .filter.views import router as filter_router

from api.v1.image.dependencies import get_image_by_id
from api.v1.image.schemas import (
    CreateImage,
    UpdateImage,
    Image as OutputImage,
    FilteredImage,
)
from core.models import db_helper, Image

router = APIRouter(prefix="/image")
router.include_router(image_filter_router)
router.include_router(filter_router)


@router.post("/all", response_model=list[FilteredImage], tags=["Image"])
async def get_images(
    filters: Annotated[List[List[str]], Body(...)],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    filter_conditions = []
    for filter_group in filters:
        or_conditions = [
            Image.filters.any(filter=filter_value) for filter_value in filter_group
        ]
        filter_conditions.append(or_(*or_conditions))

    result: Result = await session.execute(
        select(Image)
        .options(selectinload(Image.filters))
        .filter(and_(*filter_conditions))
        .order_by(Image.id)
    )

    images = result.scalars().all()
    return images


@router.post("/", tags=["Image"])
async def create_image(
    raw_image: CreateImage,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    image = Image(**raw_image.model_dump())
    session.add(image)
    await session.commit()
    return image


@router.put("/{idx}", response_model=OutputImage, tags=["Image"])
async def update_image(
    new_image: UpdateImage,
    image: Image = Depends(get_image_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_image.model_dump().items():
        setattr(image, name, value)

    await session.commit()
    return image


@router.delete("/{idx}", tags=["Image"])
async def delete_image(
    image: Image = Depends(get_image_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(image)
    await session.commit()
    return None
