"""
CRUD account methods
"""
from datetime import datetime, timedelta

from jose import JWTError, jwt

from src.app.domain.users import User
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.routers.authentication.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from src.routers.authentication.password import verify_password
from src.schemas.auth import TokenData


async def authenticate_user(
    uow: AbstractUnitOfWork, email: str, password: str
) -> User | None:
    """
    Аутентифікація користувача.
    По даним для входу шукається, перевіряється на співпадіння паролів
    та вертається User модель

    :param uow: Unit of Work
    :param email: email
    :param password: password
    :return: User якщо аутентифікація вдала, None якщо ні
    """
    async with uow:
        user = await uow.users.get("email", email)
        if not user or not verify_password(password, user.hashed_password):
            return
        return user


def create_access_token(data: dict) -> str:
    """
    Створює JWT,
    який надалі використовуватиметься для визначення залогіненого користувача.
    Шифрує у собі email користувача та дату, до якого дійсний токен.

    :param data: словник такого шаблону: {'sub': user.email}
    :return: JWT у вигляді рядка
    """
    # Час у хвилинах, під час якого токен дійсний
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_token_data(token: str) -> TokenData | None:
    """Розшифровка JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return
        return TokenData(email=email)
    except JWTError:
        return
