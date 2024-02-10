from dataclasses import dataclass

from costy.domain.models.category import CategoryId, CategoryType


@dataclass
class NewCategoryDTO:
    name: str


@dataclass
class ReadAvailableCategoriesDTO:
    ...


@dataclass
class CategoryDTO:
    id: CategoryId | None
    name: str
    kind: CategoryType
