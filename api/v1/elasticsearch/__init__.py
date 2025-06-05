from fastapi import APIRouter

from .search import router as search_router

router = APIRouter(prefix="/es")

router.include_router(search_router)
