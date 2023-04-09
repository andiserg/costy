"""
Реалізаця паттерну "Репозиторій".
Абстрактний шар між сервісним шаром та ORM
Інкапсулює більшу частину роботи з ОРМ, надаючи зрчуний інтерфейс
"""

from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.account.users.models import User
from src.app.bank_managers.models import Manager, ManagerProperty
from src.app.operations.models import Operation


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, model_object):
        raise NotImplementedError

    @abstractmethod
    async def get(self, field, value):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository, ABC):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def add(self, model_object):
        self.session.add(model_object)

    async def _get(self, model, field, value):
        return await self.session.scalar(select(model).filter_by(**{field: value}))


class UserRepository(SqlAlchemyRepository):
    async def get(self, field, value) -> User:
        return await self._get(User, field, value)


class OperationRepository(SqlAlchemyRepository):
    async def get(self, field, value) -> Operation:
        return await self._get(Operation, field, value)

    async def get_all_by_user(self, user_id) -> list[Operation]:
        return list(
            await self.session.scalars(select(Operation).filter_by(user_id=user_id))
        )


class ManagerRepository(SqlAlchemyRepository):
    async def get(self, field, value) -> Manager:
        return await self._get(Manager, field, value)

    async def get_properties(
        self, manager: Manager
    ) -> list[dict[str, str | int | float]]:
        return [
            property.as_dict
            for property in list(
                await self.session.scalars(
                    select(ManagerProperty).filter_by(manager_id=manager.id)
                )
            )
        ]

    async def add_property(self, manager: Manager, name: str, value: str | int | float):
        types = {str: "str", int: "int", float: "float"}
        self.session.add(
            ManagerProperty(
                name=name,
                value=str(value),
                type=types[type(value)],
                manager_id=manager.id,
            )
        )
