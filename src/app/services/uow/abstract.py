"""
Unit of Work: Паттерн проектування, який дозволяє слідкувати зміну об'єктів
В деяких випадках потрібно відміняти запис у базу всих об'єктів,
 якщо виникла якась помикла
Паттерн UoW допоможе в таких ситуаціях.
Також, дозволяє уникнути багаторазового з'єднання з БД для запису об'єктів
Натомість, він зберігає множину записів в рамках однієї транзакції
"""


from abc import ABC, abstractmethod

from src.app.repositories.absctract.bank_api import ABankInfoRepository
from src.app.repositories.absctract.categories import ACategoryRepository
from src.app.repositories.absctract.operations import AOperationRepository
from src.app.repositories.absctract.users import AUserRepository


class AbstractUnitOfWork(ABC):
    users: AUserRepository
    operations: AOperationRepository
    banks_info: ABankInfoRepository
    categories: ACategoryRepository

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
