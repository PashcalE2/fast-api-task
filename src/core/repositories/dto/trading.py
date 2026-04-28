from datetime import date
from dataclasses import dataclass


@dataclass
class DynamicsFilters:
    start_date: date
    end_date: date
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None


@dataclass
class TradingFilters:
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None
