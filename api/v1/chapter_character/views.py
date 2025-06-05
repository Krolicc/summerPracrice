from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.chapter_character.dependencies import get_character_chapter_by_id
from api.v1.chapter_character.schemas import (
    CreateChapterCharacter,
    UpdateChapterCharacter,
    ChapterCharacter,
)
from core.models import db_helper, character_chapter

router = APIRouter(prefix="/character_chapter", tags=["Character chapter"])


@router.get("/all", response_model=list[ChapterCharacter])
async def get_character_chapters(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(
        select(character_chapter).order_by(character_chapter.id)
    )
    character_chapters = result.scalars().all()
    return character_chapters


@router.post("/")
async def create_character_chapter(
    raw_character_chapter: CreateChapterCharacter,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    character_chapter_model = character_chapter(**raw_character_chapter.model_dump())
    session.add(character_chapter_model)
    await session.commit()
    return character_chapter_model


@router.put("/{idx}", response_model=ChapterCharacter)
async def update_character_chapter(
    new_character_chapter: UpdateChapterCharacter,
    cur_character_chapter: character_chapter = Depends(get_character_chapter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_character_chapter.model_dump().items():
        setattr(cur_character_chapter, name, value)

    await session.commit()
    return cur_character_chapter


@router.delete("/{idx}")
async def delete_date(
    character_chapter_model: character_chapter = Depends(get_character_chapter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(character_chapter_model)
    await session.commit()
    return None
