from abc import abstractmethod
from typing import Protocol, runtime_checkable

from ...domain.models.category import Category, CategoryId
from ...domain.models.user import UserId


@runtime_checkable
class CategorySaver(Protocol):
    @abstractmethod
    async def save_category(self, category: Category) -> None:
        raise NotImplementedError


@runtime_checkable
class CategoryReader(Protocol):
    @abstractmethod
    async def get_category(self, category_id: CategoryId) -> Category | None:
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
