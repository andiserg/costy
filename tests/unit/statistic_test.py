from datetime import datetime, timedelta
from random import randint

import pytest

from src.app.domain.operations import Operation
from src.app.services.statistic import get_statistic


@pytest.mark.asyncio
async def test_get_statistic():
    # TODO: Переписати без рандомних операцій і перевірити результат
    operations = [
        Operation(
            amount=randint(-10000, -10),
            description="description",
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


@pytest.mark.asyncio
async def test_statistic_by_days():
    """
    Статистика повинна містити в собі поле кількості операцій
    на кожен день у наступному вигляді:

        costs_num_by_days: dict[<date>: str, <num>: int]

    В тесті створюються операції, записується їх кількість по дням
    а потім йде перевірка на відповідність зі отриманою статистикою
    """
    operations_num_by_days = {}
    operations = []
    now = datetime.now()
    date = datetime(now.year, now.month, now.day) - timedelta(days=6)
    for _ in range(5):
        date = date + timedelta(days=1)
        opertations_num = randint(1, 10)
        operations_num_by_days[date.strftime("%Y-%m-%d")] = opertations_num
        operations += [
            Operation(
                amount=randint(-10000, -10),
                description="description",
                source_type="manual",
                time=int(date.timestamp() + randint(1, 8399)),  # random time of day
                user_id=1,
            )
            for _ in range(opertations_num)
        ]
    statistic = get_statistic(operations)
    assert statistic.costs_num_by_days == operations_num_by_days
