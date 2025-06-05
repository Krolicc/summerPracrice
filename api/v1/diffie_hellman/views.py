import string

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependecies.user_manager import get_user_manager
from api.v1.diffie_hellman.schemas import PublicKeyUpload
from api.v1.profile.dependencies import get_profile_by_id
from api.v1.user.fastapi_users import current_active_user
from core.authentication.user_manager import UserManager
from core.models import User, Profile, db_helper
from core.config import settings

router = APIRouter(prefix="/dh", tags=["Keys Diffie Hellman"])


@router.post("/public")
async def upload_dh_public_key(
    key_data: PublicKeyUpload,
    profile: Profile = Depends(get_profile_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Позволяет пользователю загрузить свой публичный ключ Диффи-Хеллмана.
    """
    if not key_data.public_key:
        raise HTTPException(status_code=400, detail="Public key cannot be empty.")

    # Можно добавить базовую валидацию формата ключа, если это Hex/Base64
    # Например, проверить, что это валидная шестнадцатеричная строка
    # if not all(
    #     c in string.hexdigits for c in key_data.public_key
    # ):  # <-- Добавьте import string
    #     raise HTTPException(
    #         status_code=400, detail="Public key must be a valid hexadecimal string."
    #     )

    # Обновляем поле dh_public_key для текущего пользователя
    profile.dh_public_key = key_data.public_key
    await session.commit()

    print(f"User {profile.id} uploaded DH public key.")
    return {"status": "success", "message": "Public key uploaded successfully."}


@router.get("/public/{user_id}")
async def get_dh_public_key(
    user_id: int,
    profile: Profile = Depends(get_profile_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Позволяет получить публичный ключ Диффи-Хеллмана другого пользователя.
    """
    stmt = select(Profile).where(Profile.id == user_id)
    result = await session.execute(stmt)
    target_profile = result.scalar_one_or_none()

    if not target_profile:
        raise HTTPException(status_code=404, detail="Target user not found.")

    if not target_profile.dh_public_key:
        raise HTTPException(
            status_code=404, detail="Target user has not uploaded a public key."
        )

    # Здесь можно добавить логику авторизации: разрешено ли current_user получить ключ target_user?
    # Например, если они в одном чате. Пока пропускаем, но это важно для реального приложения.

    print(f"User {profile.id} requested DH public key of user {target_profile.id}.")
    return {
        "user_id": str(target_profile.id),
        "public_key": target_profile.dh_public_key,
    }


# --- ЭНДПОИНТЫ ДЛЯ ПОЛУЧЕНИЯ DH ПАРАМЕТРОВ ---
@router.get("/parameters")
async def get_dh_parameters():
    """
    Предоставляет общие параметры Диффи-Хеллмана (p и g).
    """
    return {"p": settings.DH_PRIME_P, "g": settings.DH_GENERATOR_G}
