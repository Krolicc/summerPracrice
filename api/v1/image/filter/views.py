from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.image.filter.dependencies import get_filter_by_id
from api.v1.image.filter.schemas import (
    CreateFilter,
    UpdateFilter,
    Filter as OutputFilter,
)
from core.models import db_helper, Filter

router = APIRouter(prefix="/filter", tags=["Image filter"])


@router.get("/all", response_model=list[OutputFilter])
async def get_filters(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(select(Filter).order_by(Filter.id))
    filters = result.scalars().all()
    return filters


@router.post("/")
async def create_filter(
    raw_filter: CreateFilter,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    filter_model = Filter(**raw_filter.model_dump())
    session.add(filter_model)
    await session.commit()
    return filter_model


@router.put("/{idx}", response_model=OutputFilter)
async def update_filter(
    new_filter: UpdateFilter,
    cur_filter: Filter = Depends(get_filter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_filter.model_dump().items():
        setattr(cur_filter, name, value)

    await session.commit()
    return cur_filter


@router.delete("/{idx}")
async def delete_filter(
    filter_model: Filter = Depends(get_filter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(filter_model)
    await session.commit()
    return None
