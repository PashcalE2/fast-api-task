from typing import Annotated
from fastapi import APIRouter, Depends, Response, Query, status
from fastapi.encoders import jsonable_encoder

from src.core.services.trading import TradingService
from src.core.repositories.dto.trading import DynamicsFilters, TradingFilters
from src.infrastructure.api.v1 import dependencies
from src.infrastructure.api.v1.dto.trading import (
    LastDatesSchema,
    DynamicsFiltersSchema,
    TradingFiltersSchema,
    TradingResultsSchema,
)


router = APIRouter()


@router.get(path="/last-dates")
async def get_last_trading_dates(
    response: Response,
    count: Annotated[int, Query(ge=1, le=100)] = 1,
    trading_service: TradingService = Depends(dependencies.get_trading_service),
) -> LastDatesSchema:
    response.status_code = status.HTTP_200_OK
    result = await trading_service.get_last_dates(count=count)
    return LastDatesSchema(root=jsonable_encoder(result))


@router.get(path="/dynamics")
async def get_dynamics(
    response: Response,
    filters: DynamicsFiltersSchema = Depends(),
    trading_service: TradingService = Depends(dependencies.get_trading_service),
) -> TradingResultsSchema:
    response.status_code = status.HTTP_200_OK
    filters_dto = DynamicsFilters(**filters.model_dump())
    result = await trading_service.get(filters_dto)
    return TradingResultsSchema(root=jsonable_encoder(result))


@router.get(path="/results")
async def get_trading_results(
    response: Response,
    filters: TradingFiltersSchema = Depends(),
    trading_service: TradingService = Depends(dependencies.get_trading_service),
) -> TradingResultsSchema:
    response.status_code = status.HTTP_200_OK
    filters_dto = TradingFilters(**filters.model_dump())
    result = await trading_service.get_last(filters_dto)
    return TradingResultsSchema(root=jsonable_encoder(result))
