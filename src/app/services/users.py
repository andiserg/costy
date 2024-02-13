"""
CRUD операції з User сутностями
"""

from src.app.domain.users import User
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.auth.password import get_password_hash
from src.schemas.users import UserCreateSchema


async def create_user(uow: AbstractUnitOfWork, user: UserCreateSchema) -> User:
    """
    :param uow: Unit of Work
    :param user: Схема для створення користувача
    :return: src.domain.users.User
    """
    hashed_password = get_password_hash(user.password)
    async with uow:
        db_user = User(email=user.email, hashed_password=hashed_password)
        await uow.users.add(db_user)
        await uow.commit()
        return db_user


async def get_user_by_email(uow: AbstractUnitOfWork, email: str) -> User | None:
    async with uow:
        return await uow.users.get(email=email)
