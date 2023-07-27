from collections import defaultdict
from datetime import datetime

from src.app.domain.categories import Category
from src.app.domain.limits import Limit
from src.app.domain.operations import Operation
from src.app.services.statistic import get_categories_costs
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.schemas.operations import OperationCreateSchema


async def create_operation(
    uow: AbstractUnitOfWork, user_id: int, schema: OperationCreateSchema
) -> Operation | None:
    """
    Створює, добавляє в БД та повертає Operation.
    :param uow: Unit of Work
    :param user_id: ID користувача, якому налелжить операція
    :param schema: схема операції OperationCreateSchema
    :return: Operation якщо user_id існує в базі. None, якщо ні
    """
    async with uow:
        schema.time = schema.time if schema.time else int(datetime.now().timestamp())
        operation = Operation(**schema.dict(), user_id=user_id)
        await uow.operations.add(operation)
        await uow.commit()
        return operation


async def get_operations(
    uow: AbstractUnitOfWork, user_id: int, from_time=None, to_time=None
) -> list[Operation]:
    """
    Повертнення всих операцій, які містять переданий user_id в полі user_id
    :param uow: Unit of Work
    :param user_id: ID користувача, операції якого потрібно отримати
    :param from_time: початковий момент часу
    :param to_time: кінцевий момент часу
    :return: список об'єктів моделі Opetation. Якщо операцій немає, то пустий список
    """
    async with uow:
        categories = await uow.categories.get_availables(user_id)
        limits = await uow.limits.get_all(user_id)
        operations = await uow.operations.get_all_by_user(user_id, from_time, to_time)
        for operation in operations:
            # Якщо категорія операції - підкатегорія,
            # то на category_id назначається батьківська
            operation = set_subcategory_to_operation(operation, categories)
        exceeded_limits = get_exceeded_limits(operations, limits, from_time, to_time)
        operations = [
            set_exceeded_limit_prop(exceeded_limits, operation)
            for operation in operations
        ]
        return operations


def set_subcategory_to_operation(
    operation: Operation, categories: list[Category]
) -> Operation:
    if operation.category_id:
        category = next(
            category for category in categories if category.id == operation.category_id
        )
        if category.parent_id:
            operation.category_id = category.parent_id
            operation.subcategory_id = category.id
    return operation


def get_exceeded_limits(
    operations: list[Operation], limits: list[Limit], from_time=None, to_time=None
) -> dict[datetime, list[int]]:
    """
    Формування та списку категорій, які перевищили обмеження
    :param operations: список операцій
    :param limits: список обмежень
    :param from_time: з якого часу
    :param to_time: по який час
    :return: список перевищених лімітів
    """
    # from_time - Початок первого місяця періоду
    from_time = datetime.fromtimestamp(from_time).replace(day=1)
    to_time = datetime.fromtimestamp(to_time)
    # to_time - Первий день наступного місяця після остального місяця періоду
    to_time = to_time.replace(
        day=1,
        month=to_time.month + 1 if to_time.month < 12 else 12,
        hour=0,
        minute=0,
        second=0,
    )
    # Список початків місяців у періоді
    months_list = get_months_list(from_time, to_time)
    # Список операцій у кожному місяці
    operations_by_months = get_operations_by_months(operations, months_list)
    operations_categories_sum_by_months = {
        key: get_categories_costs(value) for key, value in operations_by_months.items()
    }
    exceeded_limits = defaultdict(list)
    for start_of_month, categories_costs in operations_categories_sum_by_months.items():
        for category_id, category_costs_sum in categories_costs.items():
            limit = list(limit for limit in limits if limit.category_id == category_id)
            if limit and category_costs_sum > limit[0].limit:
                exceeded_limits[start_of_month].append(category_id)
    return dict(exceeded_limits)


def get_months_list(
    from_time: datetime = None, to_time: datetime = None
) -> list[datetime]:
    months = []
    time = from_time
    while time < to_time:
        months.append(time)
        time = time.replace(month=time.month + 1)
    return months


def get_operations_by_months(
    operations: list[Operation], months: list[datetime]
) -> dict[datetime, list[Operation]]:
    result = {}
    for start_of_month in months:
        end_of_month = start_of_month.replace(month=start_of_month.month + 1)
        result[start_of_month] = [
            operation
            for operation in operations
            if start_of_month.timestamp() < operation.time < end_of_month.timestamp()
        ]
    return result


def set_exceeded_limit_prop(
    exceeded_limits: dict[datetime, list[int]], operation: Operation
) -> Operation:
    operation_time = datetime.fromtimestamp(operation.time)
    for start_of_month, categories in exceeded_limits.items():
        end_of_month = start_of_month.replace(month=start_of_month.month + 1)
        if (
            start_of_month < operation_time < end_of_month
            and operation.category_id in categories
        ):
            operation.is_exceeded_limit = True
    return operation
