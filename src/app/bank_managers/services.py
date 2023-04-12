from abc import ABC, abstractmethod
from datetime import datetime

from src.app.unit_of_work import AbstractUnitOfWork


class BankManagerRepository(ABC):
    def __init__(self, properties=None):
        self.properties = properties if properties else {}

    @abstractmethod
    def get_costs(self, from_time=datetime.now(), to_time=None):
        raise NotImplementedError


class BankManagerRepositoryFactory:
    @staticmethod
    def create_bank_manager(properties: dict) -> BankManagerRepository:
        subclasses = BankManagerRepository.__subclasses__()
        result_filter = list(
            filter(
                lambda class_: class_.__bankname__ == properties["bank_name"],
                subclasses,
            )
        )
        result_class = result_filter[0] if result_filter else None
        return result_class(properties) if result_class else None


async def get_bank_managers_by_user(
    uow: AbstractUnitOfWork, user_id: int
) -> list[BankManagerRepository]:
    async with uow:
        managers = await uow.managers.get_all_by_user(user_id)
        managers_properties = [
            await uow.managers.get_properties(manager) for manager in managers
        ]
        bank_managers = [
            BankManagerRepositoryFactory.create_bank_manager(properties)
            for properties in managers_properties
        ]
        return bank_managers


async def update_banks_costs(
    uow: AbstractUnitOfWork, managers: list[BankManagerRepository]
):
    async with uow:
        for manager in managers:
            pass
