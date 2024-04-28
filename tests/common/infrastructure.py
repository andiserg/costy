import os
from typing import AsyncGenerator, AsyncIterator

import pytest
from adaptix import Retort
from aiohttp import ClientSession
from httpx import AsyncClient
from litestar import Litestar
from pytest_asyncio import fixture
from sqlalchemy import Table
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from costy.infrastructure.db.main import get_metadata
from costy.infrastructure.db.tables import create_tables
from tests.common.app import init_test_app


@fixture(scope="session")
async def db_url() -> str:  # type: ignore
    try:
        return os.environ["TEST_DB_URL"]
    except KeyError:
        pytest.fail("TEST_DB_URL env variable not set")


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


@fixture(scope="session")
async def db_tables(db_engine: AsyncEngine) -> AsyncGenerator[None, dict[str, Table]] | None:
    metadata = get_metadata()
    tables = create_tables(metadata)

    try:
        async with db_engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)
    except OperationalError:
        pytest.fail("Connection to database is faield.")

    yield tables

    async with db_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@fixture
async def web_session() -> AsyncIterator[AsyncClient]:
    async with AsyncClient() as client:
        yield client


@fixture(scope="session")
async def app(db_url, mock_monobank_gateway) -> Litestar:
    return await init_test_app(db_url, mock_auth=True, mock_bank_gateways=mock_monobank_gateway)


@fixture
async def retort() -> Retort:
    return Retort()
