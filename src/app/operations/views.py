from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.account.auth.services import get_current_user_depend
from src.app.account.users.models import User
from src.app.operations.schemas import OperationCreateSchema, OperationSchema
from src.app.operations.services import create_operation, get_all_operations
from src.main import get_session

router = APIRouter(prefix="/operations")


@router.post("/create/", response_model=OperationSchema, status_code=201)
async def create_operation_view(
    operation_schema: OperationCreateSchema,
    current_user: User = Depends(get_current_user_depend),
    session: AsyncSession = Depends(get_session),
):
    """
    Створює в БД та повертає операцію
    :param operation_schema: JSON, який буде спаршений у OperationCretaeSchema
    :param current_user: Користувач,
     який розшифровується з токену у заголовку Authorization
    :param session: сесія БД.
    :return: Operation | Error 400
    """
    # Результат create_operation не може бути None,
    # тому що user_id не може бути не правильним.
    # У випадку помилки під час розшифровки токену
    # буде повернута помилка 401 перед виконанням тіла.
    return await create_operation(session, current_user.id, operation_schema)


@router.get("/list/", response_model=list[OperationSchema])
async def read_operations_view(
    current_user: User = Depends(get_current_user_depend),
    session: AsyncSession = Depends(get_session),
):
    """
    Повертає список операцій поточного користувача.
    TODO: Реалізувати фільтрацію
    :param current_user: Користувач,
     який розшифровується з токену у заголовку Authorization
    :param session: сесія БД.
    :return: Operation list
    """
    return await get_all_operations(session, current_user.id)
