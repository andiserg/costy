from abc import abstractmethod
from typing import Protocol, TypeAlias, TypeVar, runtime_checkable

from costy.domain.models.category import Category, CategoryId
from costy.domain.models.user import UserId
from costy.domain.sentinel import Sentinel

ParamT = TypeVar("ParamT")
SentinelOptional: TypeAlias = ParamT | None | type[Sentinel]


@runtime_checkable
class CategorySaver(Protocol):
    @abstractmethod
    async def save_category(self, category: Category) -> None:
        raise NotImplementedError


@runtime_checkable
class CategoryReader(Protocol):
    @abstractmethod
    async def get_category_by_id(self, category_id: CategoryId) -> Category | None:
        raise NotImplementedError


@runtime_checkable
class CategoryFinder(Protocol):
    @abstractmethod
    async def find_category(
        self,
        name: SentinelOptional[str] = Sentinel,
        kind: SentinelOptional[str] = Sentinel,
        user_id: SentinelOptional[UserId] = Sentinel
    ) -> Category | None:
        raise NotImplementedError


@runtime_checkable
class CategoriesReader(Protocol):
    @abstractmethod
    async def find_categories(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError


@runtime_checkable
class CategoryDeleter(Protocol):
    @abstractmethod
    async def delete_category(self, category_id: CategoryId) -> None:
        raise NotImplementedError


@runtime_checkable
class CategoryUpdater(Protocol):
    @abstractmethod
    async def update_category(self, category_id: CategoryId, category: Category) -> None:
        raise NotImplementedError


@runtime_checkable
class CategoriesFinder(Protocol):
    @abstractmethod
    async def find_categories_by_mcc_codes(self, mcc_codes: tuple[int, ...]) -> dict[int, Category]:
        raise NotImplementedError
