from dataclasses import dataclass
from typing import NewType, Optional
from enum import Enum

from costy.domain.models.user import UserId

CategoryId = NewType("CategoryId", int)


class CategoryType(Enum):
    GENERAL = "general"
    PERSONAL = "personal"


@dataclass
class Category:
    id: CategoryId | None
    name: str
    kind: CategoryType
    user_id: Optional[UserId] = None
