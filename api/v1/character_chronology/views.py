from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.character_chronology.dependencies import (
    get_character_chronology_point_by_id,
)
from api.v1.character_chronology.schemas import (
    CreateCharacterChronology,
    UpdateCharacterChronology,
    CharacterChronology,
)
from core.models import db_helper, character_chronology

router = APIRouter(prefix="/character/chronology", tags=["Character chronology"])


@router.get("/all", response_model=list[CharacterChronology])
async def get_character_chronologies(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(
        select(character_chronology).order_by(character_chronology.id)
    )
    character_chronologies = result.scalars().all()
    return character_chronologies


@router.post("/")
async def create_character_character_chronology(
    raw_character_chapter: CreateCharacterChronology,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character_chapter_model = character_chronology(**raw_character_chapter.model_dump())
    session.add(character_chapter_model)
    await session.commit()
    return character_chapter_model


@router.put("/{idx}", response_model=CharacterChronology)
async def update_character_chronology(
    new_character_chronology: UpdateCharacterChronology,
    cur_character_chronology: character_chronology = Depends(
        get_character_chronology_point_by_id
    ),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_character_chronology.model_dump().items():
        setattr(cur_character_chronology, name, value)

    await session.commit()
    return cur_character_chronology


@router.delete("/{idx}")
async def delete_character_chronology(
    character_chronology_model: character_chronology = Depends(
        get_character_chronology_point_by_id
    ),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(character_chronology_model)
    await session.commit()
    return None
