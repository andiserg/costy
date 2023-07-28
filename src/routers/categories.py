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
    Creates a record in the database and returns the operation.

    :param uow: Unit of Work
    :param category_schema: JSON, which will be parsed into CategoryCreateSchema.
    :param current_user: User decrypted from the token in the Authorization header.
    :return: Category object or Error 400.
    """
    return await create_category(uow, current_user.id, category_schema)


@router.get("/list/", response_model=list[CategorySchema])
async def read_operations_view(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Returns a list of operations for the current user.

    :param uow: Unit of Work
    :param current_user: User decrypted from the token in the Authorization header.
    :return: List of categories.
    """
    return await get_availables_categories(uow, current_user.id)
