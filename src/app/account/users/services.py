"""
CRUD операції з User сутностями
"""
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
