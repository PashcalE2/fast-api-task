import datetime
from logging import getLogger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.trading import SpimexTradingResults
from src.schemas.trading import DynamicsFiltersRequest, TradingFiltersRequest


logger = getLogger(__name__)


class TradingService:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_last_trading_dates(
        self,
        days: int,
    ) -> list[datetime.date]:
        """
        Список дат последних торговых дней (фильтрация по кол-ву последних торговых дней)
        """
        return [
            datetime.date.today(),
        ]

    async def get_dynamics(
        self,
        request: DynamicsFiltersRequest,
    ) -> list[SpimexTradingResults]:
        """
        Список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)
        """
        return [
            SpimexTradingResults(
                exchange_product_id="str",
                exchange_product_name="str",
                delivery_basis_name="str",
                volume=0,
                total=0,
                count=0,
                date=datetime.date.today(),
            )
        ]

    async def get_trading_results(
        self,
        request: TradingFiltersRequest,
    ) -> list[SpimexTradingResults]:
        """
        Список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
        """
        return [
            SpimexTradingResults(
                exchange_product_id="str",
                exchange_product_name="str",
                delivery_basis_name="str",
                volume=0,
                total=0,
                count=0,
                date=datetime.date.today(),
            )
        ]
