from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.operations import create_operation, get_operations
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.depends import get_current_user, get_uow
from src.schemas.operations import OperationCreateSchema, OperationSchema

router = APIRouter(prefix="/operations")


@router.post("/create/", response_model=OperationSchema, status_code=201)
async def create_operation_view(
    operation_schema: OperationCreateSchema,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Створює в БД та повертає операцію
    :param uow: Unit of Work
    :param operation_schema: JSON, який буде спаршений у OperationCretaeSchema
    :param current_user: Користувач,
     який розшифровується з токену у заголовку Authorization
    :return: Operation | Error 400
    """
    # Результат create_operation не може бути None,
    # тому що user_id не може бути не правильним.
    # У випадку помилки під час розшифровки токену
    # буде повернута помилка 401 перед виконанням тіла.
    return await create_operation(uow, current_user.id, operation_schema)


@router.get("/list/", response_model=list[OperationSchema])
async def read_operations_view(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
    from_time: int | None = None,
    to_time: int | None = None,
):
    """
    Повертає список операцій поточного користувача.
    TODO: Реалізувати фільтрацію
    :param uow: Unit of Work
    :param current_user: Користувач,
     який розшифровується з токену у заголовку Authorization
    :param from_time: з якого часу в unix форматі
    :param to_time: по який час в unix форматі
    :return: Operation list
    """
    from_time = from_time if from_time else int(datetime.today().timestamp())
    to_time = (
        to_time if to_time else int((datetime.today() + timedelta(days=1)).timestamp())
    )
    return await get_operations(uow, current_user.id, from_time, to_time)
