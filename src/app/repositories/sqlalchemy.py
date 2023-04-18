from abc import ABC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.absctract.base import AbstractRepository


class SqlAlchemyRepository(AbstractRepository, ABC):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def add(self, model_object):
        self.session.add(model_object)

    async def _get(self, model, field, value):
        return await self.session.scalar(select(model).filter_by(**{field: value}))
