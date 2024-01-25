from abc import abstractmethod
from typing import Protocol

from costy.domain.models.category import Category, CategoryId
from costy.domain.models.user import UserId


class CategorySaver(Protocol):
    @abstractmethod
    async def save_category(self, category: Category) -> None:
        raise NotImplementedError


class CategoryReader(Protocol):
    @abstractmethod
    async def get_category(self, category_id: CategoryId) -> Category:
        raise NotImplementedError


class CategoriesReader(Protocol):
    @abstractmethod
    async def find_categories(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError


class CategoryDeleter(Protocol):
    @abstractmethod
    async def delete_category(self, category_id: CategoryId) -> None:
        raise NotImplementedError
