from fastapi import APIRouter

from api.v1.user.fastapi_users import fastapi_users
from api.v1.user.schemas import UserRead, UserUpdate

router = APIRouter(
  prefix="/users",
  tags=["Users"],
)

# /me
# /{id}
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)