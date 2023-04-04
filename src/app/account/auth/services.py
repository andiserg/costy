"""
CRUD account methods
"""
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.app.account.auth.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from src.app.account.auth.password import verify_password
from src.app.account.users.models import User
from src.app.unit_of_work import AbstractUnitOfWork
from src.depends import get_uow
from src.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


async def get_current_user(uow: AbstractUnitOfWork, token: str) -> User | None:
    """
    Отримати User на основі JWT.

    :param uow: Unit of Work
    :param token: зашифрований JWT.
    :return: User якщо інформація валідна, інакше None
    """
    token_data = await decode_token_data(token)
    if token_data:
        async with uow:
            return await uow.users.get("email", token_data.email)


async def decode_token_data(token: str) -> TokenData | None:
    """Розшифровка JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return
        return TokenData(email=email)
    except JWTError:
        return


async def get_current_user_depend(
    uow: AbstractUnitOfWork = Depends(get_uow), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Обгортка над get_current_user для використання в якості FastApi Depends
    :return: User
    """
    result = await get_current_user(uow, token)
    if result is None:
        raise_credentials_exception()
    return result


def raise_credentials_exception():
    """
    Піднімає HTTPException.
    Викликається, якщо JWT, переданий в headers - невалідний
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    raise credentials_exception
