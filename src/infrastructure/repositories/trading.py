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


logger = getLogger(__name__)


class TradingPostgresRepository(TradingRepository):
    def __init__(self, session: AsyncSession, redis_client: Redis):
        super().__init__()
        self.session = session
        self.redis_client = redis_client

    async def get_last_dates(self, count: int) -> list[date]:
        cache_key = f"trading:{count}"
        logger.info("Looking for redis cache: key = %s", cache_key)

        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            logger.info("Found cached data")
            return [date.fromisoformat(s) for s in json_loads(cached_data)]

        stmt = (
            select(SpimexTradingResultsModel.date)
            .group_by(SpimexTradingResultsModel.date)
            .order_by(SpimexTradingResultsModel.date.desc())
            .limit(count)
        )

        logger.info("Executing SQL statement to get data")
        data = await self.session.execute(stmt)
        data = data.scalars().all()

        logger.info("Saving data to redis")
        cached_data = [d.isoformat() for d in data]
        cached_data = json_dumps(cached_data)
        await self.redis_client.set(cache_key, cached_data)

        return data

    async def get(self, filters: DynamicsFilters) -> list[SpimexTradingResults]:
        cache_key = f"trading:{mapper.dataclass_to_json(filters)}"

        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            logger.info("Found cached data")
            return [SpimexTradingResults(**d) for d in json_loads(cached_data)]

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
        data = [mapper.entity_to_domain(d) for d in data]

        logger.info("Saving data to redis")
        cached_data = mapper.dataclass_list_to_json(data)
        await self.redis_client.set(cache_key, cached_data)
        logger.info("Saved data to redis")

        return data

    async def get_last(self, filters: TradingFilters) -> list[SpimexTradingResults]:
        cache_key = f"trading:{mapper.dataclass_to_json(filters)}"

        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            logger.info("Found cached data")
            return [SpimexTradingResults(**d) for d in json_loads(cached_data)]

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
        data = [mapper.entity_to_domain(d) for d in data]

        logger.info("Saving data to redis")
        cached_data = mapper.dataclass_list_to_json(data)
        await self.redis_client.set(cache_key, cached_data)
        logger.info("Saved data to redis")
        return data
