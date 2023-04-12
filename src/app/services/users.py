"""
CRUD операції з User сутностями
"""
from src.app.account.auth.password import get_password_hash
from src.app.models.users import User
from src.app.unit_of_work import AbstractUnitOfWork
from src.schemas.users import UserCreateSchema


async def create_user(uow: AbstractUnitOfWork, user: UserCreateSchema) -> User:
    """
    :param uow: Unit of Work
    :param user: Схема для створення користувача
    :return: src.models.users.User
    """
    hashed_password = get_password_hash(user.password)
    async with uow:
        db_user = User(email=user.email, hashed_password=hashed_password)
        await uow.users.add(db_user)
        await uow.commit()
        return db_user
