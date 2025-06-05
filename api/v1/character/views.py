from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .character_body_type.views import router as body_type_router
from .character_status.views import router as status_router

from api.v1.character.dependencies import get_character_by_id
from api.v1.character.schemas import (
    CreateCharacter,
    UpdateCharacter,
    CharacterTotal,
    CharacterOne,
)
from core.models import db_helper, Character

router = APIRouter(prefix="/character")
router.include_router(body_type_router)
router.include_router(status_router)


@router.get("/{idx}/all", response_model=CharacterOne, tags=["Character"])
async def get_character(
    idx: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character: Character = await session.scalar(
        select(Character)
        .filter(Character.id == idx)
        .options(
            selectinload(Character.body_type),
            selectinload(Character.status),
            selectinload(Character.chronology_points),
        )
    )
    return character


@router.get("/all", response_model=list[CharacterTotal], tags=["Character"])
async def get_characters(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(select(Character).order_by(Character.id))
    characters = result.scalars().all()
    return characters


@router.post("/", tags=["Character"])
async def create__(
    raw_character: CreateCharacter,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character = Character(**raw_character.model_dump())
    session.add(character)
    await session.commit()
    return character


@router.put("/{idx}", response_model=CharacterTotal, tags=["Character"])
async def update_character(
    new_character: UpdateCharacter,
    character: Character = Depends(get_character_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_character.model_dump().items():
        setattr(character, name, value)

    await session.commit()
    return character


@router.delete("/{idx}", tags=["Character"])
async def delete_character(
    character: Character = Depends(get_character_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(character)
    await session.commit()
    return None
