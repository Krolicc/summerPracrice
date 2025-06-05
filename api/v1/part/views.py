from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.part.dependencies import get_part_by_id
from api.v1.part.schemas import CreatePart, UpdatePart, Part as OutputPart
from core.models import db_helper, Part

router = APIRouter(prefix="/part", tags=["Part"])


@router.get("/all", response_model=list[OutputPart])
async def get_parts(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(select(Part).order_by(Part.id))
    parts = result.scalars().all()
    return parts


@router.post("/")
async def create_part(
    raw_part: CreatePart,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    part = Part(**raw_part.model_dump())
    session.add(part)
    await session.commit()
    return part


@router.put("/{idx}", response_model=OutputPart)
async def update_part(
    new_part: UpdatePart,
    part: Part = Depends(get_part_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_part.model_dump().items():
        setattr(part, name, value)

    await session.commit()
    return part


@router.delete("/{idx}")
async def delete_part(
    part: Part = Depends(get_part_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(part)
    await session.commit()
    return None
