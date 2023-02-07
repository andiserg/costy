"""
Users endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth import get_current_user_depend
from app.crud.users import create_user
from app.main import get_session
from app.models.users import User
from app.schemas.users import UserCreateSchema, UserSchema

router = APIRouter(prefix="/users")


@router.post("/create/", response_model=UserSchema, status_code=201)
async def create_user_view(
    user: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    """
    Створення і повернення користувача
    """
    created_user = await create_user(session, user)
    return created_user


@router.get("/me/", response_model=UserSchema)
async def read_me(current_user: User = Depends(get_current_user_depend)):
    """
    Повертає залогіненого юзера, або 401, якщо юзер не вказав заголовок Authorization
    """
    return current_user
