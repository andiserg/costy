"""
Users endpoints
"""
from fastapi import APIRouter, Depends

from src.app.account.users.models import User
from src.app.account.users.services import create_user
from src.app.unit_of_work import AbstractUnitOfWork
from src.depends import get_current_user_depend, get_uow
from src.schemas.users import UserCreateSchema, UserSchema

router = APIRouter(prefix="/users")


@router.post("/create/", response_model=UserSchema, status_code=201)
async def create_user_view(
    user: UserCreateSchema, uow: AbstractUnitOfWork = Depends(get_uow)
):
    """
    Створення і повернення користувача
    """
    created_user = await create_user(uow, user)
    return created_user


@router.get("/me/", response_model=UserSchema)
async def read_me(current_user: User = Depends(get_current_user_depend)):
    """
    Повертає залогіненого юзера, або 401, якщо юзер не вказав заголовок Authorization
    """
    return current_user
