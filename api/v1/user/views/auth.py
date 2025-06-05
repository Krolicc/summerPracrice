from fastapi import APIRouter

from api.dependecies.backend import authentication_backend
from api.v1.user.fastapi_users import fastapi_users
from api.v1.user.schemas import UserRead, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(
        authentication_backend,
        # requires_verification=True,
    ),
)

# /register
router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# /verify
# /request-verify-token
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

# /forgot-password
# /reset-password
router.include_router(
    fastapi_users.get_reset_password_router(),
)
