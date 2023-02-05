"""
Налаштування бази даних
"""
import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def _get_url(test: bool = False) -> str:
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
    return f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}"


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

    def __init__(self, test: bool = False):
        self.engine = create_async_engine(_get_url(test), echo=True)
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

        # В test режимі база створюється під час ініціалізації.
        # db_created використовується як прапорець того, створена база чи ні
        self.test = test
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
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def get_session_depends(self) -> AsyncSession:
        """
        Дає AsyncSession для роботи з базою
        Увага:
            Призначена для FastApi Depends, тому що сесія повертається через yield
            В якості Depends метод відпрацює правильно,
            але виклили з інших мість можуть створити неочікувані наслідки

                database = Database()
                async with database.sessionmaker() as session:
                    <code>

            для правильного отримання сесії
        :return: sqlalchemy.ext.asyncio.AsyncSession
        """
        if self.test and not self.db_created:
            # Тут це для того, щоб виконатись у FastApi event loop
            # Якщо виконати asyncio.run(init_models()),
            # то далі робота з ORM буде неможлива
            await self.init_models()
            self.db_created = True
        async with self.sessionmaker() as session:
            yield session
