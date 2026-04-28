from datetime import date
from pydantic import BaseModel, TypeAdapter, RootModel


class TradingResultSchema(BaseModel):
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


trading_result_list_adapter = TypeAdapter(list[TradingResultSchema])


class DynamicsFilters(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None
    start_date: date = date.fromisoformat("2026-04-20")  # TODO Удалить
    end_date: date = date.fromisoformat("2026-04-28")  # TODO Удалить


class TradingFilters(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None


class LastDatesResponse(RootModel):
    root: list[date]


class TradingResultsResponse(RootModel):
    root: list[TradingResultSchema]
