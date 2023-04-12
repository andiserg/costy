"""
Реалізаця паттерну "Репозиторій".
Абстрактний шар між сервісним шаром та ORM
Інкапсулює більшу частину роботи з ОРМ, надаючи зрчуний інтерфейс
"""

from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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
