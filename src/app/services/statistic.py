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
    )
    return statistic


def get_costs_sum(operations: list[Operation]) -> int:
    """Сума витрат"""
    return sum(operation.amount for operation in operations)


def get_categories_costs(operations: list[Operation]) -> dict[int, int]:
    """Словник у форматі {<категорія>: <сума витрат по категорії>}"""
    operations_mcc = [operation.mcc for operation in operations]
    return {
        mcc: sum(
            operation.amount for operation in filter(lambda x: x.mcc == mcc, operations)
        )
        for mcc in operations_mcc
    }
