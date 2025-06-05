from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.character.character_status.dependencies import get_character_status_by_id
from api.v1.character.character_status.schemas import (
    CreateCharacterStatus,
    UpdateCharacterStatus,
    CharacterStatus as OutputCharacterStatus,
)
from core.models import db_helper, CharacterStatus

router = APIRouter(prefix="/status", tags=["Character status"])


@router.get("/all", response_model=list[OutputCharacterStatus])
async def get_character_statuses(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(
        select(CharacterStatus).order_by(CharacterStatus.id)
    )
    character_statuses = result.scalars().all()
    return character_statuses


@router.post("/")
async def create_character_status(
    raw_c_s: CreateCharacterStatus,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character_status = CharacterStatus(**raw_c_s.model_dump())
    session.add(character_status)
    await session.commit()
    return character_status


@router.put("/{idx}", response_model=OutputCharacterStatus)
async def update_character_status(
    new_character_status: UpdateCharacterStatus,
    character_status: CharacterStatus = Depends(get_character_status_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_character_status.model_dump().items():
        setattr(character_status, name, value)

    await session.commit()
    return character_status


@router.delete("/{idx}")
async def delete_character_status(
    character_status: CharacterStatus = Depends(get_character_status_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(character_status)
    await session.commit()
    return None
