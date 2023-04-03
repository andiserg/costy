"""
Реалізаця паттерну "Репозиторій".
Абстрактний шар між сервісним шаром та ORM
"""

from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.account.users.models import User
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
