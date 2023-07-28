"""
Bank Manager Repositories:

ABankInfoRepository:
Responsible for storing the BankInfo model, which contains information about the bank.

ABankManagerRepository:
Responsible for working with the bank's API.
It requires fields present in the BankInfo model.

Each bank has its own algorithm for obtaining expenses, which requires different fields.
Each subclass of ABankManagerRepository implements the work with a specific API.
"""

from abc import ABC, abstractmethod

from src.app.domain.bank_api import BankInfo
from src.app.repositories.absctract.base import AbstractRepository


class ABankInfoRepository(AbstractRepository):
    @abstractmethod
    async def get(self, field, value) -> BankInfo:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user(self, user_id) -> list[BankInfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_properties(self, manager: BankInfo) -> dict[str, str | int | float]:
        raise NotImplementedError

    @abstractmethod
    async def add_property(
        self, manager: BankInfo, name: str, value: str | int | float
    ):
        raise NotImplementedError

    @abstractmethod
    async def set_update_time_to_managers(self, ids: list[int]):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: int, bank_name: str):
        raise NotImplementedError


class ABankManagerRepository(ABC):
    __bankname__ = None
    MAX_UPDATE_PERIOD = None

    def __init__(self, properties=None):
        self.properties = properties if properties else {}

    @abstractmethod
    async def get_costs(self, from_time=None, to_time=None) -> list[dict]:
        raise NotImplementedError


class BankManagerRepositoryFactory:
    """
    Factory for creating ABankInfoRepository based on the BankInfo model.
    """

    @staticmethod
    def create_bank_manager(properties: dict) -> ABankManagerRepository:
        subclasses = ABankManagerRepository.__subclasses__()
        result_filter = list(
            filter(
                lambda class_: class_.__bankname__ == properties["bank_name"],
                subclasses,
            )
        )
        result_class = result_filter[0] if result_filter else None
        return result_class(properties) if result_class else None
