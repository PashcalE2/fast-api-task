from typing import Annotated
from fastapi import APIRouter, Depends, Response, Query, status
from fastapi.encoders import jsonable_encoder

from src.api.v1 import dependencies
from src.service.trading import TradingService
from src.schemas.trading import (
    LastDatesResponse,
    DynamicsFilters,
    TradingFilters,
    TradingResultsResponse,
)


router = APIRouter()


@router.get(path="/health")
def health() -> Response:
    return Response(content="healthy", status_code=status.HTTP_200_OK)


@router.get(path="/last-dates")
async def get_last_trading_dates(
    response: Response,
    count: Annotated[int, Query(ge=1, le=100)] = 1,
    trading_service: TradingService = Depends(dependencies.get_trading_service),
) -> LastDatesResponse:
    response.status_code = status.HTTP_200_OK
    return LastDatesResponse(
        root=jsonable_encoder(
            await trading_service.get_last_trading_dates(count=count),
        )
    )


@router.get(path="/dynamics")
async def get_dynamics(
    response: Response,
    filters: DynamicsFilters = Depends(),
    trading_service: TradingService = Depends(dependencies.get_trading_service),
) -> TradingResultsResponse:
    response.status_code = status.HTTP_200_OK
    return TradingResultsResponse(
        root=jsonable_encoder(await trading_service.get_dynamics(filters))
    )


@router.get(path="/results")
async def get_trading_results(
    response: Response,
    filters: TradingFilters = Depends(),
    trading_service: TradingService = Depends(dependencies.get_trading_service),
) -> TradingResultsResponse:
    response.status_code = status.HTTP_200_OK
    return TradingResultsResponse(
        root=jsonable_encoder(await trading_service.get_trading_results(filters))
    )
