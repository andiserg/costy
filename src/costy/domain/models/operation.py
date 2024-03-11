from dataclasses import dataclass
from typing import NewType

from costy.domain.models.category import CategoryId
from costy.domain.models.user import UserId

OperationId = NewType("OperationId", int)


@dataclass(slots=True, kw_only=True)
class Operation:
    id: OperationId | None = None
    amount: int
    description: str | None = None
    time: int
    user_id: UserId
    category_id: CategoryId | None = None
    bank_name: str | None = None
