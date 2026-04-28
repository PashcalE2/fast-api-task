from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from redis.asyncio import Redis

from src.core.repositories.trading import TradingRepository
from src.core.services.trading import TradingService
from src.infrastructure.repositories.trading import TradingPostgresRepository
from src.infrastructure.services.trading import TradingServiceImpl
from src.infrastructure.database.postgres.session import async_get_session
from src.infrastructure.database.redis.session import async_get_redis_client


async def get_trading_repository(
    session: AsyncSession = Depends(async_get_session),
    redis_client: Redis = Depends(async_get_redis_client),
) -> AsyncGenerator[TradingRepository]:
    yield TradingPostgresRepository(session=session, redis_client=redis_client)


async def get_trading_service(
    repository: TradingRepository = Depends(get_trading_repository),
) -> AsyncGenerator[TradingService, None]:
    yield TradingServiceImpl(repository=repository)
