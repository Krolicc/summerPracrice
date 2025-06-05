from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from .date.views import router as date_router

from api.v1.chronology.dependencies import get_chronology_point_by_id
from api.v1.chronology.schemas import (
    CreateChronologyPoint,
    UpdateChronologyPoint,
    ChronologyPoint,
)
from core.models import db_helper, Chronology

router = APIRouter(prefix="/chronology")
router.include_router(date_router)


@router.get("/names")
async def get_chapters():
    names = [field for field in ChronologyPoint.model_fields]
    return {
        "names": names,
    }


@router.get("/all", response_model=list[ChronologyPoint], tags=["Chronology"])
async def get_dates(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(select(Chronology).order_by(Chronology.id))
    dates = result.scalars().all()
    return dates


@router.post("/", tags=["Chronology"])
async def create_date(
    raw_date: CreateChronologyPoint,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    date = Chronology(**raw_date.model_dump())
    session.add(date)
    await session.commit()
    return date


@router.put("/{idx}", response_model=ChronologyPoint, tags=["Chronology"])
async def update_date(
    new_date: UpdateChronologyPoint,
    date: Chronology = Depends(get_chronology_point_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_date.model_dump().items():
        setattr(date, name, value)

    await session.commit()
    return date


@router.delete("/{idx}", tags=["Chronology"])
async def delete_date(
    date: Chronology = Depends(get_chronology_point_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(date)
    await session.commit()
    return None
