from datetime import date
from dataclasses import asdict
from logging import getLogger
from json import loads as json_loads, dumps as json_dumps
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.core.domain.trading import SpimexTradingResults
from src.core.repositories.trading import TradingRepository
from src.core.repositories.dto.trading import DynamicsFilters, TradingFilters
from src.infrastructure.database.postgres.models.trading import (
    SpimexTradingResultsModel,
)
from src.infrastructure.mappers.trading import TradingMapper as mapper
from src.infrastructure.database.redis.utils import get_expiration_time


logger = getLogger(__name__)


class TradingPostgresRepository(TradingRepository):
    def __init__(self, session: AsyncSession, redis_client: Redis):
        super().__init__()
        self.session = session
        self.redis_client = redis_client

    async def _redis_get_last_dates(self, key: str) -> list[date] | None:
        logger.info("Looking for redis cache: key = %s", key)

        cached_data = await self.redis_client.get(key)
        if cached_data:
            logger.info("Found cached data")
            return [date.fromisoformat(s) for s in json_loads(cached_data)]

        return None

    async def _db_get_last_dates(self, count: int) -> list[date]:
        stmt = (
            select(SpimexTradingResultsModel.date)
            .group_by(SpimexTradingResultsModel.date)
            .order_by(SpimexTradingResultsModel.date.desc())
            .limit(count)
        )

        logger.info("Executing SQL statement to get data")
        data = await self.session.execute(stmt)
        return data.scalars().all()

    async def _redis_set_last_dates(self, key: str, data: list[date]) -> None:
        logger.info("Saving data to redis")
        data = [d.isoformat() for d in data]
        data = json_dumps(data)
        await self.redis_client.setex(
            key=key,
            time=get_expiration_time(),
            value=data,
        )

    async def get_last_dates(self, count: int) -> list[date]:
        key = f"trading:{count}"
        data = await self._redis_get_last_dates(key)
        if data:
            return data

        data = await self._db_get_last_dates(count)
        await self._redis_set_last_dates(key, data)

        return data

    async def _redis_get(self, key: str) -> list[SpimexTradingResults] | None:
        cached_data = await self.redis_client.get(key)
        if cached_data:
            logger.info("Found cached data")
            return [SpimexTradingResults(**d) for d in json_loads(cached_data)]
        return None

    async def _db_get(self, filters: DynamicsFilters) -> list[SpimexTradingResults]:
        stmt = (
            select(SpimexTradingResultsModel)
            .order_by(
                SpimexTradingResultsModel.exchange_product_id,
                SpimexTradingResultsModel.date,
            )
            .where(
                SpimexTradingResultsModel.date >= filters.start_date,
                SpimexTradingResultsModel.date <= filters.end_date,
            )
        )

        for field, value in asdict(filters).items():
            if not hasattr(SpimexTradingResultsModel, field) or value is None:
                continue
            stmt = stmt.where(getattr(SpimexTradingResultsModel, field) == value)

        logger.info("Executing SQL statement to get data")
        data = await self.session.execute(stmt)
        data = data.scalars().all()
        return [mapper.entity_to_domain(d) for d in data]

    async def _redis_set(self, key: str, data: list[SpimexTradingResults]) -> None:
        logger.info("Saving data to redis")
        data = mapper.dataclass_list_to_json(data)
        await self.redis_client.setex(
            key=key,
            time=get_expiration_time(),
            value=data,
        )
        logger.info("Saved data to redis")

    async def get(self, filters: DynamicsFilters) -> list[SpimexTradingResults]:
        key = f"trading:{mapper.dataclass_to_json(filters)}"
        data = await self._redis_get(key)
        if data:
            return data

        data = await self._db_get(filters)
        await self._redis_set(key, data)

        return data

    async def _redis_get_last(self, key: str) -> list[SpimexTradingResults] | None:
        data = await self.redis_client.get(key)
        if data:
            logger.info("Found cached data")
            return [SpimexTradingResults(**d) for d in json_loads(data)]
        return None

    async def _db_get_last(self, filters: TradingFilters) -> list[SpimexTradingResults]:
        stmt = (
            select(SpimexTradingResultsModel)
            .where(
                SpimexTradingResultsModel.date
                == select(func.max(SpimexTradingResultsModel.date)).scalar_subquery()
            )
            .order_by(SpimexTradingResultsModel.exchange_product_id)
        )

        for field, value in asdict(filters).items():
            if not hasattr(SpimexTradingResultsModel, field) or value is None:
                continue
            stmt = stmt.where(getattr(SpimexTradingResultsModel, field) == value)

        logger.info("Executing SQL statement to get data")
        data = await self.session.execute(stmt)
        data = data.scalars().all()
        return [mapper.entity_to_domain(d) for d in data]

    async def _redis_set_last(self, key: str, data: list[SpimexTradingResults]) -> None:
        logger.info("Saving data to redis")
        data = mapper.dataclass_list_to_json(data)
        await self.redis_client.setex(
            key=key,
            time=get_expiration_time(),
            value=data,
        )
        logger.info("Saved data to redis")

    async def get_last(self, filters: TradingFilters) -> list[SpimexTradingResults]:
        key = f"trading:{mapper.dataclass_to_json(filters)}"
        data = await self._redis_get_last(key)
        if data:
            return data

        data = await self._db_get_last(filters)
        await self._redis_set_last(key, data)

        return data
