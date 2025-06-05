from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.chronology.date.dependencies import get_date_by_id
from api.v1.chronology.date.schemas import CreateDate, UpdateDate, Date as OutputDate
from core.models import db_helper, Date

router = APIRouter(prefix="/date", tags=["Date"])


@router.get("/names")
async def get_chapters():
    names = [field for field in OutputDate.model_fields]
    return {
        "names": names,
    }


@router.get("/all", response_model=list[OutputDate])
async def get_dates(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(select(Date).order_by(Date.id))
    dates = result.scalars().all()
    return dates


@router.get("/{idx}", response_model=OutputDate)
async def get_dates(date: Date = Depends(get_date_by_id)):
    return date


@router.post("/", response_model=OutputDate)
async def create_date(
    raw_date: CreateDate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    date = Date(**raw_date.model_dump())
    session.add(date)
    await session.commit()
    return date


@router.put("/{idx}", response_model=OutputDate)
async def update_date(
    new_date: UpdateDate,
    date: Date = Depends(get_date_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_date.model_dump().items():
        setattr(date, name, value)

    await session.commit()
    return date


@router.delete("/{idx}")
async def delete_date(
    date: Date = Depends(get_date_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(date)
    await session.commit()
    return None
