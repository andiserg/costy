"""
Unit of Work: Паттерн проектування, який дозволяє слідкувати зміну об'єктів
В деяких випадках потрібно відміняти запис у базу всих об'єктів,
 якщо виникла якась помикла
Паттерн UoW допоможе в таких ситуаціях.
Також, дозволяє уникнути багаторазового з'єднання з БД для запису об'єктів
Натомість, він зберігає множину записів в рамках однієї транзакції
"""

from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.bank_managers.bank_managers import ManagerRepository
from src.app.repositories.operations import OperationRepository
from src.app.repositories.users import UserRepository


class AbstractUnitOfWork(ABC):
    users: UserRepository
    operations: OperationRepository
    managers: ManagerRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

    async def commit(self):
        await self._commit()

    @abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.users = UserRepository(self.session)
        self.operations = OperationRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()
        return True

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
