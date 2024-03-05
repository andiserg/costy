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


@dataclass
class UpdateCategoryData:
    name: str


@dataclass
class UpdateCategoryDTO:
    category_id: CategoryId
    data: UpdateCategoryData
