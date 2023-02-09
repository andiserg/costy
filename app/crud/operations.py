from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operations import Operation
from app.schemas.operations import OperationCreateSchema


async def create_operation(
    session: AsyncSession, user_id: int, schema: OperationCreateSchema
) -> Operation | None:
    """
    Створює, добавляє в БД та повертає Operation.
    :param session: сесія БД.
    :param user_id: ID користувача, якому налелжить операція
    :param schema: схема операції OperationCreateSchema
    :return: Operation якщо user_id існує в базі. None, якщо ні
    """
    operation = Operation(**schema.dict(), user_id=user_id)
    session.add(operation)
    try:
        await session.commit()
        return operation
    except IntegrityError:
        return


async def get_all_operations(session: AsyncSession, user_id: int) -> list[Operation]:
    """
    Повертає всі операції які містять переданий user_id в полі user_id
    :param session: сесія БД
    :param user_id: ID користувача, операції якого потрібно отримати
    :return: список об'єктів моделі Opetation. Якщо операцій немає, то пустий список
    """
    result = await session.scalars(
        select(Operation).filter(Operation.user_id == user_id + 1)
    )
    return list(result)
