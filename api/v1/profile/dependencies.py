from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user.fastapi_users import current_active_user
from core.models import Profile, db_helper, User


async def get_profile_by_id(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    profile: Profile = await session.scalar(
        select(Profile).filter(Profile.id == user.id)
    )

    if profile is None:
        profile = Profile(user_id=user.id)

        session.add(profile)
        await session.commit()

    return profile
