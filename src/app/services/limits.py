from src.app.domain.limits import Limit
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.schemas.limits import LimitCreateSchema


async def create_limit(
    uow: AbstractUnitOfWork, user_id: int, schema: LimitCreateSchema
) -> Limit | None:
    """
    Створення та добавлення в БД сутності Limit
    :param uow: Unit Of Work
    :param user_id: ID користувача
    :param schema: LimitCreateSchema
    :return: Limit якщо user_id існує в базі. None, якщо ні
    """
    async with uow:
        limit = Limit(**schema.dict(), user_id=user_id)
        await uow.limits.add(limit)
        await uow.commit()
        return limit


async def get_limits(uow: AbstractUnitOfWork, user_id: int) -> list[Limit]:
    async with uow:
        limits = await uow.limits.get_all(user_id)
        return limits
