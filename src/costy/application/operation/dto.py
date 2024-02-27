from dataclasses import dataclass
from datetime import datetime

from costy.domain.models.category import CategoryId


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
