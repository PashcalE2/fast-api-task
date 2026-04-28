from abc import ABC, abstractmethod
from datetime import date

from src.core.repositories.dto.trading import DynamicsFilters, TradingFilters
from src.core.domain.trading import SpimexTradingResults


class TradingRepository(ABC):
    @abstractmethod
    async def get_last_dates(self, count: int) -> list[date]: ...

    @abstractmethod
    async def get(self, filters: DynamicsFilters) -> list[SpimexTradingResults]: ...

    @abstractmethod
    async def get_last(self, filters: TradingFilters) -> list[SpimexTradingResults]: ...
