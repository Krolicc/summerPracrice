from fastapi import APIRouter

from .user.views.auth import router as auth_router
from .user.views.users import router as users_router
from .profile.views import router as profile_router
from .room.views import router as room_router

from .character.views import router as character_router

from .image.views import router as image_router

from .part.views import router as part_router
from .chapter.views import router as chapter_router

from .chronology.views import router as chronology_router

from .chapter_character.views import router as chapter_character_router
from .character_chronology.views import router as character_chronology_router
from .profile_chapter.views import router as profile_chapter_router

from .general_views import router as general_router

# from .mongo import router as mongo_router
# from .elasticsearch import router as es_router
from .kafka import router as kafka_router
from .websocket import router as ws_router
from .diffie_hellman.views import router as dh_router

router = APIRouter(
    prefix="/v1",
)


router.include_router(character_router)

router.include_router(image_router)

router.include_router(chapter_router)
router.include_router(part_router)

router.include_router(chronology_router)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(profile_router)
router.include_router(room_router)

router.include_router(chapter_character_router)
router.include_router(character_chronology_router)
router.include_router(profile_chapter_router)

router.include_router(general_router)

# router.include_router(mongo_router)
# router.include_router(es_router)
router.include_router(kafka_router)
router.include_router(ws_router)
router.include_router(dh_router)
