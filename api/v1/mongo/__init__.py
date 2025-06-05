from fastapi import APIRouter

from .image.views import router as image_router

router = APIRouter(
    prefix="/mongo",
)

router.include_router(image_router)
