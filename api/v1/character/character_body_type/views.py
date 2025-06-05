from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.character.character_body_type.dependencies import get_body_type_by_id
from api.v1.character.character_body_type.schemas import (
    CreateBodyType,
    UpdateBodyType,
    BodyType as OutputBodyType,
)
from core.models import db_helper, CharacterBodyType

router = APIRouter(prefix="/body-type", tags=["Character body type"])


@router.get("/all", response_model=list[OutputBodyType])
async def get_body_types(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(
        select(CharacterBodyType).order_by(CharacterBodyType.id)
    )
    body_types = result.scalars().all()
    return body_types


@router.post("/")
async def create_body_type(
    raw_body_type: CreateBodyType,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    body_type = CharacterBodyType(**raw_body_type.model_dump())
    session.add(body_type)
    await session.commit()
    return body_type


@router.put("/{idx}", response_model=OutputBodyType)
async def update_body_type(
    new_body_type: UpdateBodyType,
    body_type: CharacterBodyType = Depends(get_body_type_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_body_type.model_dump().items():
        setattr(body_type, name, value)

    await session.commit()
    return body_type


@router.delete("/{idx}")
async def delete_body_type(
    body_type: CharacterBodyType = Depends(get_body_type_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(body_type)
    await session.commit()
    return None
