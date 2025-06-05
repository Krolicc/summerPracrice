from fastapi import APIRouter

from .table_names import router as table_names_router
from .column_names import router as column_names_router
from .generate_presigned_url import router as generate_presigned_url_router

router = APIRouter(
    prefix="/general",
    tags=["General"],
)

router.include_router(table_names_router)
router.include_router(column_names_router)
router.include_router(generate_presigned_url_router)
