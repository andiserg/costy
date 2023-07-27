from collections import Counter
from datetime import datetime

from src.app.domain.operations import Operation
from src.app.domain.statistic import Statistic


def get_statistic(operations: list[Operation]) -> Statistic:
    """
    Створення статистики витрат користувача
    :param operations: Список операцій
    :return: Statistic
    """
    statistic = Statistic(
        costs_sum=get_costs_sum(operations),
        categories_costs=get_categories_costs(operations),
        costs_num_by_days=get_costs_num_by_days(operations),
        costs_sum_by_days=get_costs_sum_by_days(operations),
    )
    return statistic


def get_costs_sum(operations: list[Operation]) -> int:
    """Сума витрат"""
    return sum(operation.amount for operation in operations)


def get_categories_costs(operations: list[Operation]) -> dict[int, int]:
    """Словник у форматі {<категорія>: <сума витрат по категорії>}"""
    categories_id = [operation.category_id for operation in operations]

    return {
        category_id: sum(
            operation.amount
            for operation in filter(
                lambda op: op.category_id == category_id, operations
            )
        )
        for category_id in categories_id
    }


def get_costs_num_by_days(operations: list[Operation]) -> dict[str, int]:
    costs_num_by_days = Counter()
    for operation in operations:
        costs_num_by_days[
            datetime.fromtimestamp(operation.time).strftime("%Y-%m-%d")
        ] += 1
    return dict(costs_num_by_days)


def get_costs_sum_by_days(operations: list[Operation]) -> dict[str, int]:
    costs_num_by_days = Counter()
    for operation in operations:
        costs_num_by_days[
            datetime.fromtimestamp(operation.time).strftime("%Y-%m-%d")
        ] += operation.amount
    return dict(costs_num_by_days)
