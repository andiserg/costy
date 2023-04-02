"""
CRUD account methods
"""
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.account.auth.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from src.app.account.auth.password import verify_password
from src.app.account.auth.schemas import TokenData
from src.app.account.users.models import User
from src.app.account.users.services import get_user_by_email
from src.main import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> User | None:
    """
    Аутентифікація користувача.
    По даним для входу шукається, перевіряється на співпадіння паролів
    та вертається User модель

    :param session: сесія ДБ
    :param email: email
    :param password: password
    :return: User якщо аутентифікація вдала, None якщо ні
    """
    user = await get_user_by_email(session=session, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return
    return user


def create_access_token(data: dict) -> str:
    """
    Створює JSON Web Token (JWT),
    який надалі використовуватиметься для визначення залогіненого користувача.
    Шифрує у собі email користувача та дату, до якого дійсний токен.

    :param data: словник такого шаблону: {'sub': user.email}
    :return: JWT у вигляді рядка
    """
    # Час у хвилинах, під час якого токен дійсний
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(session: AsyncSession, token: str) -> User | None:
    """
    Повертає User на основі JWT.
    Розшифровує токен, дістає з нього email та якщо всі дані валідні,
    то дістає та повертає об'єкт моделі User з бази.

    :param session: сесія ДБ.
    :param token: зашифрований JWT.
    :return: User якщо інформація валідна, інакше None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return
        token_data = TokenData(email=email)
    except JWTError:
        return
    return await get_user_by_email(session, email=token_data.email)


async def get_current_user_depend(
    session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Обгортка над get_current_user для використання в якості FastApi Depends
    :return: src.models.user.User
    """
    result = await get_current_user(session, token)
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
