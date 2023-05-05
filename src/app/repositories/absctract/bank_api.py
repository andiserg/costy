"""
Репозиторії менеджерів банку

ABankInfoRepository:
    Відповідає за зберігання моделі BankInfo
    яка містить інформацію про банк

ABankManagerRepository:
    Відповідає за роботу з API банка. Для роботи потрібні поля
    які находяться в BankInfo моделі

    Кожен банк має свій алгоритм для отримання витрат, для якого потрібні різні поля.
    Кожен нащадок ABankManagerRepository реалізує роботу з якимось API.
"""

from abc import ABC, abstractmethod

from src.app.domain.bank_api import BankInfo
from src.app.domain.operations import Operation
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


class ABankManagerRepository(ABC):
    __bankname__ = None
    MAX_UPDATE_PERIOD = None

    def __init__(self, properties=None):
        self.properties = properties if properties else {}

    @abstractmethod
    async def get_costs(self, from_time=None, to_time=None) -> list[Operation]:
        raise NotImplementedError


class BankManagerRepositoryFactory:
    """
    Фабрика для створення ABankInfoRepository на основі BankInfo моделі
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
