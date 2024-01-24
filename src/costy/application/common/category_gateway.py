from typing import Protocol

from costy.domain.models.category import CategoryId, Category
from costy.domain.models.user import UserId


class CategorySaver(Protocol):
    async def save_category(self, category: Category) -> CategoryId:
        raise NotImplementedError


class CategoryReader(Protocol):
    async def get_category(self, category_id: CategoryId) -> Category:
        raise NotImplementedError


class CategoriesReader(Protocol):
    async def find_categories(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError


class CategoryDeleter(Protocol):
    async def delete_category(self, category_id: CategoryId) -> None:
        raise NotImplementedError
