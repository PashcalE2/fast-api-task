from datetime import date
from pydantic import BaseModel


class DynamicsFiltersRequest(BaseModel):
    oil_id: str
    delivery_type_id: str
    delivery_basis_id: str
    start_date: date
    end_date: date


class TradingFiltersRequest(BaseModel):
    oil_id: str
    delivery_type_id: str
    delivery_basis_id: str


class LastDatesResponse(BaseModel):
    dates: list


class TradingResultsResponse(BaseModel):
    tradings: list
