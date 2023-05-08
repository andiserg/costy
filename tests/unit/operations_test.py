from datetime import datetime, timedelta

import pytest

from src.app.domain.operations import Operation
from src.app.services.operations import create_operation, get_operations
from src.schemas.operations import OperationCreateSchema
from tests.fake_adapters.uow import FakeUnitOfWork


@pytest.mark.asyncio
async def test_create_operation():
    uow = FakeUnitOfWork()
    schema = OperationCreateSchema(
        amount=100, description="test", mcc=9999, source_type="manual"
    )
    operation = await create_operation(uow, 1, schema)
    assert operation


@pytest.mark.asyncio
async def test_read_operation():
    uow = FakeUnitOfWork()
    async with uow:
        uow.operations.instances = [
            Operation(
                id=1,
                amount=100,
                description="test",
                mcc=9999,
                source_type="manual",
                time=int(datetime.now().timestamp()),
                user_id=1,
            ),
            Operation(
                id=2,
                amount=333,
                description="test",
                mcc=9998,
                source_type="manual",
                time=int(datetime.now().timestamp()),
                user_id=1,
            ),
            Operation(
                id=3,
                amount=150,
                description="test",
                mcc=9999,
                source_type="manual",
                time=int(datetime.now().timestamp()),
                user_id=1,
            ),
        ]
        operations = await get_operations(
            uow,
            1,
            (datetime.now() - timedelta(minutes=1)).timestamp(),
            datetime.now().timestamp(),
        )
        assert len(operations) == 3
