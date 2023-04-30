"""
Налаштування бази даних
"""
import os

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from src.app.adapters.orm import create_tables, start_mappers


def _get_url(test: bool = False, async_: bool = True) -> str:
    """
    :param test: Якщо True, то підставляє назву тестової бази в URL
    :return: URL для підлключення до БД
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
    Клас роботи з базою даних, який використовується у програмі.

    Містить два головних атрибути:
        engine - об'єкт для роботи з драйверами бази даних
        sessionmaker - фабрика для створення сесії роботи з engine

    Тестовий режим:
        Якщо вказати test = True під час ініціалізації,
        то буде створений об'єкт тестової бази, яка використовує іншу базу в роботі.
        Використовується під час pytest тестів.
    """

    def __init__(self, mapper_registry, test: bool = False):
        self.engine = create_async_engine(_get_url(test), echo=True)
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)
        self.mapper_registry = mapper_registry

        self.test = test
        # db_created використовується як прапорець того, створена база чи ні
        self.db_created = False

    async def init_models(self):
        """
        Створює базу даних в test режимі.

        AsyncSession не підтримує такі методи як
            Base.metadata.drop_all
            Base.metadata.create_all
        тому ці методи виконуються у синхронному режимі за допомогою run_sync
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(self.mapper_registry.metadata.drop_all)
            await conn.run_sync(self.mapper_registry.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        """
        Дає AsyncSession для роботи з базою
        Увага:
            Призначена для FastApi Depends, тому що сесія повертається через yield
            В якості Depends метод відпрацює правильно,
            але виклили з інших мість можуть створити неочікувані наслідки.
        :return: sqlalchemy.ext.asyncio.AsyncSession
        """
        if self.test and not self.db_created:
            # Тут це для того, щоб виконатись у async event loop
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
    Фабрика для бази даних.

    Для налаштування бази даних, потрібно прив'язати класи до таблиць.
    Таку операцію потрібно проводити один раз за сесію,
     тому що ОРМ не дасть повторно прив'язати одні і ті самі класи.
     Фабрика реалізує патерн "Singleton", що дозволяє їй один раз провести прив'язку
     та за потребності повертати об'єкти бази даних.
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
    Перезапис залежності сесії бази даних.
    В цілях уникнення глобальних змінних, в коді використовується функція-заглушка
     для залежності сесії
    А під час налаштування, викликається ця функція, яка перезаписує залежність
     на працюючу функцію
    """
    app.dependency_overrides[get_session_depend] = database.get_session


async def get_session_depend():
    """Функція-заглушка"""
    pass
