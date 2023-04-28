from datetime import datetime

from src.app.domain.operations import Operation
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
        return await uow.operations.get_all_by_user(user_id, from_time, to_time)
