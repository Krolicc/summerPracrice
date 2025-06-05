from fastapi import APIRouter

from .send_message_fragment import router as kafka_router

router = APIRouter(
    prefix="/kafka",
)

router.include_router(kafka_router)
