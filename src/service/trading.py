from json import loads as json_loads, dumps as json_dumps
from datetime import date
from logging import getLogger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.database.models.trading import SpimexTradingResults
from src.schemas.trading import (
    TradingResultSchema,
    trading_result_list_adapter,
    DynamicsFilters,
    TradingFilters,
)


logger = getLogger(__name__)
# TODO Cache expiration time
# TODO Спросить про пагинацию?


class TradingService:
    def __init__(self, session: AsyncSession, redis_client: Redis):
        self.session = session
        self.redis_client = redis_client

    async def get_last_trading_dates(
        self,
        count: int,
    ) -> list[date]:
        """
        Список дат последних торговых дней (фильтрация по кол-ву последних торговых дней)
        """
        cache_key = f"trading:{count}"
        logger.info("Looking for redis cache: key = %s", cache_key)

        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            logger.info("Found cached data")
            return [date.fromisoformat(s) for s in json_loads(cached_data)]

        stmt = (
            select(SpimexTradingResults.date)
            .group_by(SpimexTradingResults.date)
            .order_by(SpimexTradingResults.date.desc())
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

    async def get_dynamics(
        self,
        filters: DynamicsFilters,
    ) -> list[TradingResultSchema]:
        """
        Список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)
        """

        cache_key = f"trading:{filters.model_dump_json()}"

        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            logger.info("Found cached data")
            return trading_result_list_adapter.validate_json(cached_data)

        stmt = (
            select(SpimexTradingResults)
            .order_by(
                SpimexTradingResults.exchange_product_id, SpimexTradingResults.date
            )
            .where(
                SpimexTradingResults.date >= filters.start_date,
                SpimexTradingResults.date <= filters.end_date,
            )
        )

        for field, value in filters.model_dump().items():
            if not hasattr(SpimexTradingResults, field) or value is None:
                continue
            stmt = stmt.where(getattr(SpimexTradingResults, field) == value)

        logger.info("Executing SQL statement to get data")
        data = await self.session.execute(stmt)
        data = data.scalars().all()
        data = [TradingResultSchema.model_validate(d) for d in data]

        logger.info("Saving data to redis")
        cached_data = trading_result_list_adapter.dump_json(data)
        await self.redis_client.set(cache_key, cached_data)
        logger.info("Saved data to redis")
        return data

    async def get_trading_results(
        self,
        filters: TradingFilters,
    ) -> list[TradingResultSchema]:
        """
        Список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
        """
        cache_key = f"trading:{filters.model_dump_json()}"

        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            logger.info("Found cached data")
            return trading_result_list_adapter.validate_json(cached_data)

        stmt = (
            select(SpimexTradingResults)
            .where(
                SpimexTradingResults.date
                == select(func.max(SpimexTradingResults.date)).scalar_subquery()
            )
            .order_by(SpimexTradingResults.exchange_product_id)
        )

        for field, value in filters.model_dump().items():
            if not hasattr(SpimexTradingResults, field) or value is None:
                continue
            stmt = stmt.where(getattr(SpimexTradingResults, field) == value)

        logger.info("Executing SQL statement to get data")
        data = await self.session.execute(stmt)
        data = data.scalars().all()
        data = [TradingResultSchema.model_validate(d) for d in data]

        logger.info("Saving data to redis")
        cached_data = trading_result_list_adapter.dump_json(data)
        await self.redis_client.set(cache_key, cached_data)
        logger.info("Saved data to redis")
        return data
