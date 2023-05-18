from abc import abstractmethod

from src.app.domain.categories import Category
from src.app.repositories.absctract.base import AbstractRepository


class ACategoryRepository(AbstractRepository):
    @abstractmethod
    async def get(self, **kwargs) -> Category:
        raise NotImplementedError

    @abstractmethod
    async def _get_categories(self, *args) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def get_availables(self, user_id) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def get_categories_in_values(
        self, field: str, values: list
    ) -> list[Category]:
        raise NotImplementedError
