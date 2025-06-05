from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.profile_chapter.dependencies import get_profile_chapter_by_id
from api.v1.profile_chapter.schemas import (
    CreateProfileChapter,
    UpdateProfileChapter,
    ProfileChapter as OutputProfileChapter,
)
from core.models import db_helper, ProfileChapter

router = APIRouter(prefix="/profile/chapter", tags=["Profile chapter"])


@router.get("/all", response_model=list[OutputProfileChapter])
async def get_profile_chapters(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(
        select(ProfileChapter).order_by(ProfileChapter.id)
    )
    profile_chapter = result.scalars().all()
    return profile_chapter


@router.post("/")
async def create_profile_chapter(
    raw_profile_chapter: CreateProfileChapter,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    profile_chapter = ProfileChapter(**raw_profile_chapter.model_dump())
    session.add(profile_chapter)
    await session.commit()
    return profile_chapter


@router.put("/{idx}", response_model=OutputProfileChapter)
async def update_profile_chapter(
    new_profile_chapter: UpdateProfileChapter,
    profile_chapter: ProfileChapter = Depends(get_profile_chapter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_profile_chapter.model_dump().items():
        setattr(profile_chapter, name, value)

    await session.commit()
    return profile_chapter


@router.delete("/{idx}")
async def delete_profile_chapter(
    profile_chapter: ProfileChapter = Depends(get_profile_chapter_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(profile_chapter)
    await session.commit()
    return None
