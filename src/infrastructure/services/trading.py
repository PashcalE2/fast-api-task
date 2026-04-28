from datetime import date
from logging import getLogger

from src.core.services.trading import TradingService
from src.core.repositories.dto.trading import DynamicsFilters, TradingFilters
from src.core.domain.trading import SpimexTradingResults


logger = getLogger(__name__)


class TradingServiceImpl(TradingService):
    async def get_last_dates(
        self,
        count: int,
    ) -> list[date]:
        """
        Список дат последних торговых дней (фильтрация по кол-ву последних торговых дней)
        """
        return await self.repository.get_last_dates(count=count)

    async def get(
        self,
        filters: DynamicsFilters,
    ) -> list[SpimexTradingResults]:
        """
        Список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)
        """
        return await self.repository.get(filters=filters)

    async def get_last(
        self,
        filters: TradingFilters,
    ) -> list[SpimexTradingResults]:
        """
        Список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
        """
        return await self.repository.get_last(filters=filters)
