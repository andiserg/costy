import time

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.adapters.repository import OperationRepository
from src.app.operations.models import Operation
from src.app.operations.schemas import OperationCreateSchema


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
    operation = Operation(**schema.dict(), unix_time=time.time(), user_id=user_id)
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
    operations = OperationRepository(session)
    return await operations.get_all_by_user(user_id)
