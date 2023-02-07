from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import get_user_by_email
from app.crypt.password import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(email: str, password: str, session: AsyncSession):
    """
    Аутентифікація користувача. По даним для входу шукається та вертається user
    :param email: email
    :param password: password
    :param session: сесія ДБ
    :return: User якщо аутентифікація вдала, None якщо ні
    """
    user = await get_user_by_email(session=session, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
