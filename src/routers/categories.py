from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.categories import create_category, get_availables_categories
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.depends import get_current_user, get_uow
from src.schemas.categories import CategoryCreateSchema, CategorySchema

router = APIRouter(prefix="/categories")


@router.post("/create/", response_model=CategorySchema, status_code=201)
async def create_operation_view(
    category_schema: CategoryCreateSchema,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Створює в БД та повертає операцію
    :param uow: Unit of Work
    :param category_schema: JSON, який буде спаршений у CategoryCretaeSchema
    :param current_user: Користувач,
     який розшифровується з токену у заголовку Authorization
    :return: Category | Error 400
    """
    # Результат create_category не може бути None,
    # тому що user_id не може бути не правильним.
    # У випадку помилки під час розшифровки токену
    # буде повернута помилка 401 перед виконанням тіла.
    return await create_category(uow, current_user.id, category_schema)


@router.get("/list/", response_model=list[CategorySchema])
async def read_operations_view(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Повертає список операцій поточного користувача.
    :param uow: Unit of Work
    :param current_user: Користувач,
     який розшифровується з токену у заголовку Authorization
    :return: Category list
    """
    return await get_availables_categories(uow, current_user.id)
