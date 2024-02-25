from dataclasses import dataclass
from enum import Enum
from typing import NewType, Optional

from costy.domain.models.user import UserId

CategoryId = NewType("CategoryId", int)


class CategoryType(Enum):
    GENERAL = "general"
    PERSONAL = "personal"


@dataclass
class Category:
    id: CategoryId | None
    name: str
    kind: str = CategoryType.GENERAL.value
    user_id: Optional[UserId] = None
