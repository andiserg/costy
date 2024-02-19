import pytest
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from costy.infrastructure.config import SettingError


def get_engine(url: str) -> AsyncEngine:
    try:
        return create_async_engine(url, future=True)
    except SettingError:
        pytest.skip("Auth settings env var are not exists.")


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine)


def get_metadata() -> MetaData:
    return MetaData()
