from typing import AsyncGenerator, AsyncIterator

import pytest
from adaptix import Retort
from httpx import AsyncClient
from pytest_asyncio import fixture
from sqlalchemy import delete
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from auth import tables as auth_tables
from costy.infrastructure.db import tables as costy_tables


@fixture(scope="session")
async def db_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url, future=True)


@fixture(scope="session")
async def db_sessionmaker(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(db_engine)


@fixture(scope="session")
async def db_session(db_sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
    session = db_sessionmaker()
    yield session


@fixture(autouse=True)
async def rollback_session(db_session):
    yield
    await db_session.rollback()


@fixture
async def clean_up_db(module, db_session):
    yield
    tables = {
        "costy": (costy_tables.bankapis, costy_tables.operations, costy_tables.categories),
        "auth": (auth_tables.users,)
    }
    for table in tables[module]:
        await db_session.execute(delete(table))
    await db_session.commit()


@fixture(scope="session", autouse=True)
async def db_tables(module, db_engine: AsyncEngine) -> AsyncGenerator[None, None] | None:
    metadatas = {
        "costy": costy_tables.metadata,
        "auth": auth_tables.metadata
    }
    metadata = metadatas[module]

    try:
        async with db_engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)
    except OperationalError:
        pytest.fail("Connection to database is faield.")

    yield None

    async with db_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@fixture
async def web_session() -> AsyncIterator[AsyncClient]:
    async with AsyncClient() as client:
        yield client


@fixture
async def retort() -> Retort:
    return Retort()
