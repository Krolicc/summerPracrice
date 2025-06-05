from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Room, db_helper


async def get_room_by_id(
    room_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    room: Room = await session.scalar(select(Room).filter(Room.id == room_id))

    return room
