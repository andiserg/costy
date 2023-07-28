"""
Database Configuration
"""
import os

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from src.app.adapters.orm import create_tables, start_mappers


def _get_url(test: bool = False, async_: bool = True) -> str:
    """
    :param test: If True, then substitutes the name of the test database into the URL.
    :return: URL for connecting to the database.
    """
    db_name = os.getenv("DB_NAME") if not test else os.getenv("TEST_DB_NAME")
    db_user, db_password, db_host = (
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
    )
    return (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}"
        if async_
        else f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
    )


class Database:
    """
    Class for working with the database used in the program.
    Contains two main attributes:
    engine - an object for working with database drivers
    sessionmaker - a factory for creating database sessions with the engine

    Test mode:
    If 'test' is set to True during initialization,
    then a test database object will be created,
    which uses a different database in the program.
    It is used during pytest tests.
    """

    def __init__(self, mapper_registry, test: bool = False):
        self.engine = create_async_engine(_get_url(test))
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)
        self.mapper_registry = mapper_registry

        self.test = test
        # The variable db_created is used as a flag
        # to indicate whether the database has been created or not.
        self.db_created = False

    async def init_models(self):
        """
        Creates the database in test mode.

        AsyncSession does not support methods like
        Base.metadata.drop_all and
        Base.metadata.create_all.
        Therefore, these methods are executed in synchronous mode using run_sync.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(self.mapper_registry.metadata.drop_all)
            await conn.run_sync(self.mapper_registry.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        """
        Provides an AsyncSession for working with the database.
        Attention:
            Designed for FastApi Depends because the session is returned using yield.
            When used as a Depends method, it works correctly.
            However, calling it from other places may lead to unexpected consequences.
        :return: sqlalchemy.ext.asyncio.AsyncSession
        """
        if self.test and not self.db_created:
            # Here, this is to be executed in the async event loop.
            await self.init_models()
            self.db_created = True
        async with self.sessionmaker() as session:
            yield session


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseFactory(metaclass=SingletonMeta):
    """
    Database factory.

    To configure the database, it is necessary to bind classes to tables.
    This operation needs to be performed once per session since
    the ORM does not allow re-binding the same classes.
    The factory implements the "Singleton" pattern,
    which allows it to perform the binding only
    once and then return database objects as needed.
    """

    def __init__(self):
        self.mapper_registry = registry()
        self._bootstrap_tables()

    def _bootstrap_tables(self):
        tables = create_tables(self.mapper_registry)
        start_mappers(self.mapper_registry, tables)

    def get_database(self, test=False) -> Database:
        return Database(self.mapper_registry, test=test)


def bind_database_to_app(app: FastAPI, database: Database):
    """
    Overriding the database session dependency.
    To avoid global variables, a dummy function
    is used in the code as a session dependency.
    During setup, this function is called to
    override the dependency with the actual working function.
    """
    app.dependency_overrides[get_session_depend] = database.get_session


async def get_session_depend():
    """Dummy function"""
    pass
