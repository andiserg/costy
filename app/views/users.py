"""
Users endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import create_user
from app.main import get_session
from app.schemas.users import UserCreateSchema, UserSchema

router = APIRouter()


@router.post("/users/create/", response_model=UserSchema)
async def create_user_view(
    user: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    """
    Створення і повернення користувача
    """
    created_user = await create_user(session, user)
    return created_user
