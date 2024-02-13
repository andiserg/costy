"""
Users endpoints
"""

from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.app.services.users import create_user
from src.depends import get_current_user, get_uow
from src.schemas.users import UserCreateSchema, UserSchema

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserSchema, status_code=201)
async def create_user_view(
    user: UserCreateSchema, uow: AbstractUnitOfWork = Depends(get_uow)
):
    """
    Creation and retrieval of the user.
    :param user: user create info
    :param uow: unit of work (fastapi depend)
    :return: UserSchema
    """
    created_user = await create_user(uow, user)
    return created_user


@router.get("/", response_model=UserSchema)
async def read_me(current_user: User = Depends(get_current_user)):
    """
    Returns the logged-in user or 401
    if the user did not provide the Authorization header.
    :param current_user: user (fastapi depend)
    :return: UserSchema or 401
    """
    return current_user
