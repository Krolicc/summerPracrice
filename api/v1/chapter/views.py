from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.chapter.dependencies import get_chapter_by_id
from api.v1.chapter.schemas import (
    CreateChapter,
    UpdateChapter,
    Chapter as OutputChapter,
)
from core.models import db_helper, Chapter

router = APIRouter(prefix="/chapter", tags=["Chapter"])


@router.get("/all", response_model=list[OutputChapter])
async def get_chapters(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(select(Chapter).order_by(Chapter.id))
    chapters = result.scalars().all()
    return chapters


@router.post("/")
async def create_chapter(
    raw_chapter: CreateChapter,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    chapter = Chapter(**raw_chapter.model_dump())
    session.add(chapter)
    await session.commit()
    return chapter


@router.put("/{idx}", response_model=OutputChapter)
async def update_chapter(
    new_chapter: UpdateChapter,
    chapter: Chapter = Depends(get_chapter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_chapter.model_dump().items():
        setattr(chapter, name, value)

    await session.commit()
    return chapter


@router.delete("/{idx}")
async def delete_date(
    chapter: Chapter = Depends(get_chapter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(chapter)
    await session.commit()
    return None
