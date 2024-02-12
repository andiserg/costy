"""
Поширені функції, які перевикористовуються в багатьох тестах.
Створені для того, щоб писати одинакового коду у різних файлах (DRY)
"""

import random

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.users import User
from src.app.services.uow.sqlalchemy import SqlAlchemyUnitOfWork
from src.app.services.users import create_user
from src.schemas.users import UserCreateSchema


async def create_user_with_orm(session: AsyncSession) -> User:
    """
    Створення та повернення юзера за допомогою AsyncSession
    :param session: SqlAlchemy session
    :return: User
    """
    user_schema = UserCreateSchema(  # nosec B106
        email="test@test.com", password="123456"
    )
    uow = SqlAlchemyUnitOfWork(session)
    return await create_user(uow, user_schema)


async def create_func_user(client: AsyncClient) -> dict:
    """
    Створення та повернення юзера за допомогою AsyncClient
    :param client: httpx.AsyncClient
    :return: dict з інформацією про користувача
    """
    user_data = {"email": "test@mail.test", "password": "123456"}  # nosec B106
    return (await client.post("/users/", json=user_data)).json()


async def create_and_auth_func_user(client: AsyncClient) -> dict:
    """
    Створює, логінить та повертає юзера за допомогою AsyncClient
    :param client: httpx.AsyncClient
    :return: {token: str, user: dict} де:
        - token: готовий токен у вигляді "<token_type> <access_token>",
         який можна зразу використовувати у якості заголовка
        - user: словник з інформацією про юзера
    """
    created_user = await create_func_user(client)
    token_response = (
        await client.post(
            "/token/",
            data={"username": "test@mail.test", "password": "123456"},  # nosec B106
        )
    ).json()
    token_result = f"{token_response['token_type']} {token_response['access_token']}"
    return {"token": token_result, "user": created_user}


async def create_operations(headers: dict, client: AsyncClient):
    for _ in range(10):
        operation_data = {
            "amount": random.randint(-10000, -10),
            "description": "description",
            "mcc": random.randint(1000, 9999),
            "source_type": "manual",
        }
        await client.post("/operations/", json=operation_data, headers=headers)
