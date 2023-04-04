import random
import time

import pytest

from src.app.account.users.services import create_user
from src.app.operations.models import Operation
from src.app.operations.services import create_operation
from src.app.unit_of_work import SqlAlchemyUnitOfWork
from src.schemas.operations import OperationCreateSchema
from src.schemas.users import UserCreateSchema
from tests.config import database, precents_evn_variables  # noqa: F401;


@pytest.mark.asyncio
@precents_evn_variables
async def test_create_operation(database):  # noqa: F811;
    """
    Перевірка створення Operation
    """
    async with database.sessionmaker() as session:
        uow = SqlAlchemyUnitOfWork(session)
        user_schema = UserCreateSchema(email="test", password="test")  # nosec B106
        created_user = await create_user(uow, user_schema)

        operation_schema = OperationCreateSchema(
            amount=-1000,
            description="description",
            unix_time=time.time(),
            mcc=9999,
            source_type="manual",
        )
        operation = await create_operation(uow, created_user.id, operation_schema)
        assert isinstance(operation, Operation)

        # Спроба створити операції з неправильним ID користувача
        incorrect_operation = await create_operation(uow, 999, operation_schema)
        assert incorrect_operation is None


@pytest.mark.asyncio
@precents_evn_variables
async def test_read_operations(database):  # noqa: F811;
    """
    Перевірка різних методів отримання списку операцій, з фільтраціями і без.
    """
    async with database.sessionmaker() as session:
        uow = SqlAlchemyUnitOfWork(session)
        user_schema = UserCreateSchema(email="test", password="test")  # nosec B106
        created_user = await create_user(uow, user_schema)

        for _ in range(10):
            operation_schema = OperationCreateSchema(
                amount=random.randint(-10000, -10),
                description="description",
                unix_time=time.time(),
                mcc=random.randint(1000, 9999),
                source_type="manual",
            )
            await create_operation(uow, created_user.id, operation_schema)

        async with uow:
            operations = await uow.operations.get_all_by_user(created_user.id)
            assert isinstance(operations, list)
            assert isinstance(operations[0], Operation)
            assert len(operations) == 10
