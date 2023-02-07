"""
CRUD auth methods
"""
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import get_user_by_email
from app.crypt.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.crypt.password import verify_password
from app.models.users import User
from app.schemas.auth import TokenData

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
