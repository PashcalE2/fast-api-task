from datetime import date
from pydantic import BaseModel, RootModel, model_validator


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
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be >= start_date")
        return self


class TradingFiltersSchema(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None


class LastDatesSchema(RootModel):
    root: list[date]


class TradingResultsSchema(RootModel):
    root: list[TradingResultsSchema]
