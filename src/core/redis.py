from logging import getLogger
from typing import AsyncGenerator
from redis.asyncio import Redis, ConnectionPool

from src.core.settings import settings


logger = getLogger(__name__)

pool = ConnectionPool.from_url(
    settings.redis.url,
    max_connections=settings.redis.max_connections,
    decode_responses=settings.redis.decode_responses,
)


async def async_get_redis_client() -> AsyncGenerator[Redis]:
    logger.info("Creating Redis client")
    redis_client = Redis(connection_pool=pool)
    yield redis_client
    logger.info("Closing Redis client")
    await redis_client.close()
