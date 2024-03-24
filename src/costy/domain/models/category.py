from dataclasses import dataclass
from enum import Enum
from typing import NewType

from costy.domain.models.user import UserId

CategoryId = NewType("CategoryId", int)


class CategoryType(Enum):
    GENERAL = "general"
    PERSONAL = "personal"
    BANK = "bank"


@dataclass(slots=True, kw_only=True)
class Category:
    id: CategoryId | None = None
    name: str
    kind: str = CategoryType.GENERAL.value
    user_id: UserId | None = None
