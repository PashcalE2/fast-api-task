from abc import ABC, abstractmethod
from datetime import date

from src.core.repositories.trading import TradingRepository
from src.core.repositories.dto.trading import DynamicsFilters, TradingFilters
from src.core.domain.trading import SpimexTradingResults


class TradingService(ABC):
    def __init__(self, repository: TradingRepository):
        super().__init__()
        self.repository = repository

    @abstractmethod
    async def get_last_dates(self, count: int) -> list[date]: ...

    @abstractmethod
    async def get(self, filters: DynamicsFilters) -> list[SpimexTradingResults]: ...

    @abstractmethod
    async def get_last(self, filters: TradingFilters) -> list[SpimexTradingResults]: ...
