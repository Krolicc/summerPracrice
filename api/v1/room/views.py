from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Result, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.profile.dependencies import get_profile_by_id
from api.v1.room.dependencies import get_room_by_id
from api.v1.room.schemas import (
    CreateRoom,
    UpdateRoom,
    Room as OutputRoom,
)
from core.models import db_helper, Room, Profile

router = APIRouter(prefix="/room", tags=["Room"])


@router.get("/all", response_model=list[OutputRoom])
async def get_rooms(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result: Result = await session.execute(select(Room).order_by(Room.id))
    rooms = result.scalars().all()
    return rooms


@router.post("/connect/{room_id}", response_model=OutputRoom)
async def connect_to_room(
    profile: Profile = Depends(get_profile_by_id),
    room: Room = Depends(get_room_by_id),
    session=Depends(db_helper.session_getter),
):
    if room is None:
        raise HTTPException(404)

    if room.interlocutor_id is not None and not (room.interlocutor_id == profile.id):
        raise HTTPException(403)

    room.interlocutor_id = profile.id

    await session.commit()

    return room


@router.get("/{room_id}", response_model=OutputRoom)
async def get_room(
    room: Room = Depends(get_room_by_id),
):
    return room


@router.get("/", response_model=list[OutputRoom])
async def get_user_rooms(
    profile: Profile = Depends(get_profile_by_id),
    session=Depends(db_helper.session_getter),
):
    result: Result = await session.execute(
        select(Room)
        .where(
            or_(
                Room.creator_id == profile.id,
                Room.interlocutor_id == profile.id,
            )
        )
        .order_by(Room.id)
    )

    rooms = result.scalars().all()
    return rooms


@router.post("/")
async def create_room(
    raw_room: CreateRoom,
    profile: Profile = Depends(get_profile_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    room_model = Room(
        **raw_room.model_dump(), creator_id=profile.id, interlocutor_id=None
    )
    session.add(room_model)
    await session.commit()
    return room_model


@router.put("/{idx}", response_model=OutputRoom)
async def update_room(
    new_room: UpdateRoom,
    room: Room = Depends(get_room_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    for name, value in new_room.model_dump().items():
        setattr(room, name, value)

    await session.commit()
    return room


@router.delete("/{idx}")
async def delete_room(
    room: Room = Depends(get_room_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await session.delete(room)
    await session.commit()
    return None
