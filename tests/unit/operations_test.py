import random
import time
from datetime import datetime, timedelta

import pytest

from src.app.domain.operations import Operation
from src.app.services.operations import create_operation, get_operations
from src.app.services.uow.sqlalchemy import SqlAlchemyUnitOfWork
from src.app.services.users import create_user
from src.schemas.operations import OperationCreateSchema
from src.schemas.users import UserCreateSchema
from tests.conftest import precents_evn_variables  # noqa: F401;


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
                unix_time=datetime.now().timestamp(),
                mcc=random.randint(1000, 9999),
                source_type="manual",
            )
            await create_operation(uow, created_user.id, operation_schema)

        operations = await get_operations(
            uow,
            created_user.id,
            from_time=int((datetime.now() - timedelta(minutes=1)).timestamp()),
            to_time=int(datetime.now().timestamp()),
        )
        assert isinstance(operations, list)
        assert isinstance(operations[0], Operation)
        assert len(operations) == 10


@pytest.mark.asyncio
@precents_evn_variables
async def test_read_operations_in_date_range(database):
    async with database.sessionmaker() as session:
        uow = SqlAlchemyUnitOfWork(session)
        user_schema = UserCreateSchema(email="test", password="test")  # nosec B106
        user = await create_user(uow, user_schema)

        todays_operation_schema = OperationCreateSchema(
            amount=random.randint(-10000, -10),
            description="description",
            time=datetime.now().timestamp(),
            mcc=random.randint(1000, 9999),
            source_type="manual",
        )
        await create_operation(uow, user.id, todays_operation_schema)
        async with uow:
            yesterdays_operation = Operation(
                amount=random.randint(-10000, -10),
                description="description",
                time=int((datetime.now() - timedelta(days=1)).timestamp()),
                mcc=random.randint(1000, 9999),
                source_type="manual",
                user_id=user.id,
            )
            await uow.operations.add(yesterdays_operation)
            await uow.commit()

        today = datetime.today().timestamp()
        tomorrow = (datetime.today() + timedelta(days=1)).timestamp()
        operations = await get_operations(
            uow, user.id, from_time=int(today), to_time=int(tomorrow)
        )
        assert len(operations) == 1
