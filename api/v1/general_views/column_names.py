from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

router = APIRouter(
    prefix="/column_names",
)


@router.get("/{name}")
async def get_column_names(
    name: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        connection = await session.connection()
        try:
            columns = await connection.run_sync(
                lambda conn: inspect(conn).get_columns(name)
            )
            return {"columns": [column["name"] for column in columns]}
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Table '{name}' not found: {str(e)}",
            )
