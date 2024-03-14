from dataclasses import dataclass
from datetime import datetime

from costy.domain.models.category import CategoryId
from costy.domain.models.operation import OperationId
from costy.domain.sentinel import Sentinel


@dataclass(kw_only=True)
class NewOperationDTO:
    amount: int
    description: str | None = None
    time: int = int(datetime.now().timestamp())
    category_id: CategoryId


@dataclass
class ListOperationDTO:
    from_time: int | None
    to_time: int | None


@dataclass(kw_only=True)
class UpdateOperationData:
    amount: int | None = None
    description: str | None | type[Sentinel] = Sentinel
    time: int | None = None
    category_id: CategoryId | None | type[Sentinel] = Sentinel


@dataclass
class UpdateOperationDTO:
    operation_id: OperationId
    data: UpdateOperationData
