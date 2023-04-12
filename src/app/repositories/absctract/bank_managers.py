from abc import abstractmethod

from src.app.models.bank_managers import Manager
from src.app.repositories.absctract.base import AbstractRepository


class AManagerRepository(AbstractRepository):
    @abstractmethod
    async def get(self, field, value) -> Manager:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user(self, user_id) -> list[Manager]:
        raise NotImplementedError

    @abstractmethod
    async def get_properties(self, manager: Manager) -> dict[str, str | int | float]:
        raise NotImplementedError

    @abstractmethod
    async def add_property(self, manager: Manager, name: str, value: str | int | float):
        raise NotImplementedError
