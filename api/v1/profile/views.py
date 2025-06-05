from fastapi import APIRouter, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.profile.dependencies import get_profile_by_id
from api.v1.profile.schemas import (
    CreateProfile,
    UpdateProfile,
    Profile as OutputProfile,
)
from core.models import db_helper, Profile

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/all", response_model=list[OutputProfile])
async def get_profiles(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(select(Profile).order_by(Profile.id))
    profiles = result.scalars().all()
    return profiles


@router.get("/current", response_model=OutputProfile)
async def get_profiles(profile=Depends(get_profile_by_id)):
    return profile


@router.post("/")
async def create_profile(
    raw_profile: CreateProfile,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    profile_model = Profile(**raw_profile.model_dump())
    session.add(profile_model)
    await session.commit()
    return profile_model


@router.put("/{idx}", response_model=OutputProfile)
async def update_profile(
    new_profile: UpdateProfile,
    profile: Profile = Depends(get_profile_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_profile.model_dump().items():
        setattr(profile, name, value)

    await session.commit()
    return profile


@router.delete("/{idx}")
async def delete_profile(
    profile: Profile = Depends(get_profile_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(profile)
    await session.commit()
    return None
