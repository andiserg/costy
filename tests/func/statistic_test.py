import random
from datetime import datetime

import pytest

from src.app.domain.operations import Operation
from src.app.services.statistic import get_statistic
from src.database import Database


@pytest.mark.asyncio
async def test_get_statistic(database: Database):
    operations = [
        Operation(
            amount=random.randint(-10000, -10),
            description="description",
            mcc=random.randint(9996, 9999),
            source_type="manual",
            time=int(datetime.now().timestamp()),
            user_id=1,
        )
        for _ in range(10)
    ]
    statistic = get_statistic(operations)
    print(1)
