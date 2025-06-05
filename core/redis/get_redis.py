from redis.asyncio import Redis
from core.config import settings


async def get_redis():
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        # password="your_password",
        decode_responses=True,
    )
    try:
        yield redis
    finally:
        await redis.close()
