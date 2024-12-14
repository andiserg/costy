from dataclasses import dataclass
from enum import Enum
from typing import NewType

CategoryId = NewType("CategoryId", int)


class CategoryType(Enum):
    GENERAL = "general"
    PERSONAL = "personal"


@dataclass(slots=True, kw_only=True)
class Category:
    id: CategoryId | None = None
    name: str
    kind: str = CategoryType.GENERAL.value
    user_id: int | None = None
    view: dict[str, str] | None = None
