from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.account.users.models import User
from src.app.operations.models import Operation


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, model):
        raise NotImplementedError

    @abstractmethod
    def get(self, field, value):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository, ABC):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _get(self, model, field, value):
        return await self.session.scalar(select(model).filter_by(**{field: value}))


class UserRepository(SqlAlchemyRepository):
    def add(self, user):
        self.session.add(user)

    async def get(self, field, value) -> User:
        return await self._get(User, field, value)


class OperationRepository(SqlAlchemyRepository):
    def add(self, operation):
        self.session.add(operation)

    async def get(self, field, value) -> Operation:
        return await self._get(Operation, field, value)
