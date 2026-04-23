from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.database.session import async_get_session
from src.service.trading import TradingService


async def get_trading_service(
    session: AsyncSession = Depends(async_get_session),
) -> AsyncGenerator[TradingService, None]:
    yield TradingService(session)
