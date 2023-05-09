import random
from datetime import datetime, timedelta

import pytest

from src.app.domain.operations import Operation
from src.app.repositories.operations import OperationRepository
from tests.patterns import create_user_with_orm


@pytest.mark.asyncio
async def test_create_and_read_operations(database):
    async with database.sessionmaker() as session:
        repository = OperationRepository(session)
        created_user = await create_user_with_orm(session)
        for _ in range(10):
            await repository.add(
                Operation(
                    amount=random.randint(10, 10000),
                    description="description",
                    time=int(datetime.now().timestamp()),
                    mcc=random.randint(1000, 9999),
                    source_type="manual",
                    user_id=created_user.id,
                )
            )
        await session.commit()

        operations = await repository.get_all_by_user(
            created_user.id,
            int((datetime.now() - timedelta(minutes=1)).timestamp()),
            int(datetime.now().timestamp()),
        )
        assert len(operations) == 10
