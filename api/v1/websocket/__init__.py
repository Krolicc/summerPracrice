from fastapi import APIRouter

from .endpoint import router as ws_router

router = APIRouter(tags=["Web Socket"])

router.include_router(ws_router)
