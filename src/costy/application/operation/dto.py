from dataclasses import dataclass

from costy.domain.models.category import CategoryId


@dataclass
class NewOperationDTO:
    amount: int
    description: str | None
    time: int
    category_id: CategoryId


@dataclass
class ListOperationDTO:
    from_time: int | None
    to_time: int | None
