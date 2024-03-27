from dataclasses import dataclass

from costy.domain.models.category import CategoryId
from costy.domain.sentinel import Sentinel, SentinelOptional


@dataclass(slots=True, kw_only=True)
class NewCategoryDTO:
    name: str
    view: dict | None = None


@dataclass
class ReadAvailableCategoriesDTO:
    ...


@dataclass(slots=True, kw_only=True)
class UpdateCategoryData:
    name: str | None = None
    view: SentinelOptional[dict] = Sentinel


@dataclass
class UpdateCategoryDTO:
    category_id: CategoryId
    data: UpdateCategoryData
