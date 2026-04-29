from dataclasses import asdict
from json import dumps as json_dumps

from src.core.domain.trading import SpimexTradingResults
from src.infrastructure.database.postgres.models.trading import (
    SpimexTradingResultsModel,
)


class TradingMapper:
    @staticmethod
    def entity_to_domain(ent: SpimexTradingResultsModel) -> SpimexTradingResults:
        return SpimexTradingResults(
            exchange_product_id=ent.exchange_product_id,
            date=ent.date,
            exchange_product_name=ent.exchange_product_name,
            oil_id=ent.oil_id,
            delivery_basis_id=ent.delivery_basis_id,
            delivery_basis_name=ent.delivery_basis_name,
            delivery_type_id=ent.delivery_type_id,
            volume=ent.volume,
            total=ent.total,
            count=ent.count,
        )

    @staticmethod
    def dataclass_to_json(obj) -> str:
        return json_dumps(asdict(obj), default=str)

    @staticmethod
    def dataclass_list_to_json(objs: list) -> str:
        return json_dumps([asdict(obj) for obj in objs], default=str)
