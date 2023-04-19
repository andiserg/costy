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
        operation = Operation(
            **schema.dict(), time=int(datetime.now().timestamp()), user_id=user_id
        )
        await uow.operations.add(operation)
        await uow.commit()
        return operation


async def get_all_operations(uow: AbstractUnitOfWork, user_id: int) -> list[Operation]:
    """
    Повертає всі операції які містять переданий user_id в полі user_id
    :param uow: Unit of Work
    :param user_id: ID користувача, операції якого потрібно отримати
    :return: список об'єктів моделі Opetation. Якщо операцій немає, то пустий список
    """
    async with uow:
        operations = await uow.operations.get_all_by_user(user_id)
        return list(operations)
