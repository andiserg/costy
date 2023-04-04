from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.unit_of_work import SqlAlchemyUnitOfWork
from src.main import get_session


def get_uow(session: AsyncSession = Depends(get_session)):
    """Використовується в якості FastApi Depends"""
    yield SqlAlchemyUnitOfWork(session)
