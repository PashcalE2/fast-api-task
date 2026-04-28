from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from redis.asyncio import Redis

from src.database.session import async_get_session
from src.service.trading import TradingService
from src.core.redis import async_get_redis_client


async def get_trading_service(
    session: AsyncSession = Depends(async_get_session),
    redis_client: Redis = Depends(async_get_redis_client),
) -> AsyncGenerator[TradingService, None]:
    yield TradingService(session=session, redis_client=redis_client)
