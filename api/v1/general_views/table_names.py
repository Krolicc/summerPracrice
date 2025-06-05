from fastapi import APIRouter, Depends
from sqlalchemy import MetaData, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

router = APIRouter(
    prefix="/table_names",
)

__table_args__ = {
    "filter": "image/filter",
    "image_filter": "image/_/filter",
    "character_status": "character/status",
    "character_body_type": "character/body-type",
    "date": "chronology/date",
}


@router.get("/")
async def get_table_names(session: AsyncSession = Depends(db_helper.session_getter)):
    exclude_table_names = [
        "alembic_version",
        "access_token",
        "user",
    ]

    async with session.begin():
        connection = await session.connection()
        table_names = await connection.run_sync(
            lambda conn: inspect(conn).get_table_names()
        )

        filtered_table_names = [
            tn for tn in table_names if tn not in exclude_table_names
        ]

        return {
            "table_names": filtered_table_names,
            "aliases": __table_args__,
        }
