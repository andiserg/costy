from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.account.auth.services import get_current_user
from src.app.account.users.models import User
from src.app.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from src.core.database import get_session_depend

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_uow(session: AsyncSession = Depends(get_session_depend)):
    yield SqlAlchemyUnitOfWork(session)


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
