from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.image.image_filter.dependencies import get_image_filter_by_id
from api.v1.image.image_filter.schemas import (
    CreateImageFilter,
    UpdateImageFilter,
    ImageFilter as OutputImageFilter,
)
from core.models import db_helper, image_filter

router = APIRouter(prefix="/_/filter", tags=["Image_Filter"])


@router.get("/all", response_model=list[OutputImageFilter])
async def get_image_filters(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(
        select(image_filter).order_by(image_filter.id)
    )
    image_filters = result.scalars().all()
    return image_filters


@router.post("/")
async def create_image_filter(
    raw_image_filter: CreateImageFilter,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    image_filter_model = image_filter(**raw_image_filter.model_dump())
    session.add(image_filter_model)
    await session.commit()
    return image_filter_model


@router.put("/{idx}", response_model=OutputImageFilter)
async def update_image_filter(
    new_image_filter: UpdateImageFilter,
    image_filter_model: image_filter = Depends(get_image_filter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_image_filter.model_dump().items():
        setattr(image_filter_model, name, value)

    await session.commit()
    return image_filter_model


@router.delete("/{idx}")
async def delete_image_filter(
    image_filter_model: image_filter = Depends(get_image_filter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(image_filter_model)
    await session.commit()
    return None
