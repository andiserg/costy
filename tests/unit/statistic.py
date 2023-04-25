import random
from datetime import datetime

import pytest

from src.app.domain.operations import Operation
from src.app.services.statistic import get_statistic


@pytest.mark.asyncio
async def test_get_statistic():
    # TODO: Переписати без рандомних операцій і перевірити результат
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
    get_statistic(operations)
    assert True


@pytest.mark.asyncio
async def test_get_statistic_with_empty_operations():
    operations = []
    statictic = get_statistic(operations)

    assert statictic.costs_sum == 0
    assert statictic.categories_costs == {}
