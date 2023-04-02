"""
CRUD операції з User сутностями
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.account.auth.password import get_password_hash
from src.app.account.users.models import User
from src.app.account.users.schemas import UserCreateSchema


async def create_user(session: AsyncSession, user: UserCreateSchema) -> User:
    """
    :param session: Сесія ДБ. Див. src.database.database.Database
    :param user: Схема для створення користувача
    :return: src.models.users.User
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    await session.commit()
    return db_user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    """
    :param session: Сесія ДБ. Див. src.database.database.Database
    :param user_id: ID користувача
    :return: src.models.users.User
    :return: None, якщо користувача з таким ID не існує
    """
    return await session.scalar(select(User).filter(User.id == user_id))


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """
    :param session: Сесія ДБ. Див. src.database.database.Database
    :param email: Email користувача
    :return: src.models.users.User
    :return: None, якщо користувача з таким email не існує
    """
    return await session.scalar(select(User).filter(User.email == email))
