from datetime import date
from dataclasses import dataclass


@dataclass
class SpimexTradingResults:
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
