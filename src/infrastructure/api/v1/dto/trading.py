from datetime import date
from pydantic import BaseModel, RootModel


class TradingResultsSchema(BaseModel):
    exchange_product_id: str
    date: "date"
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int

    class Config:
        from_attributes = True


class DynamicsFiltersSchema(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None
    start_date: date = date.fromisoformat("2026-04-20")
    end_date: date = date.fromisoformat("2026-04-28")


class TradingFiltersSchema(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None


class LastDatesSchema(RootModel):
    root: list[date]


class TradingResultsSchema(RootModel):
    root: list[TradingResultsSchema]
