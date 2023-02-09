import random
import time

import pytest

from app.crud.operations import create_operation, get_all_operations
from app.crud.users import create_user
from app.models.operations import Operation
from app.schemas.operations import OperationCreateSchema
from app.schemas.users import UserCreateSchema
from app.tests.config import database, precents_evn_variables  # noqa: F401;


@pytest.mark.asyncio
@precents_evn_variables
async def test_create_operation(database):  # noqa: F811;
    """
    Перевірка створення Operation
    """
    async with database.sessionmaker() as session:
        user_schema = UserCreateSchema(email="test", password="test")  # nosec B106
        created_user = await create_user(session, user_schema)

        operation_schema = OperationCreateSchema(
            amount=-1000,
            description="description",
            unix_time=time.time(),
            mcc=9999,
            source_type="manual",
        )
        operation = await create_operation(session, created_user.id, operation_schema)
        assert isinstance(operation, Operation)

        # Спроба створити операції з неправильним ID користувача
        incorrect_operation = await create_operation(session, 999, operation_schema)
        assert incorrect_operation is None


@pytest.mark.asyncio
@precents_evn_variables
async def test_read_operations(database):  # noqa: F811;
    """
    Перевірка різних методів отримання списку операцій, з фільтраціями і без.
    """
    async with database.sessionmaker() as session:
        user_schema = UserCreateSchema(email="test", password="test")  # nosec B106
        created_user = await create_user(session, user_schema)

        for _ in range(10):
            operation_schema = OperationCreateSchema(
                amount=random.randint(-10000, -10),
                description="description",
                unix_time=time.time(),
                mcc=random.randint(1000, 9999),
                source_type="manual",
            )
            await create_operation(session, created_user.id, operation_schema)

        operations = await get_all_operations(session, created_user.id)
        assert isinstance(operations, list)
        assert isinstance(operations[0], Operation)
        assert len(operations) == 10