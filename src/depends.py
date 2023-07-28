"""
Dependencies for FastApi routers.
These methods are used with the Depends
construct to obtain the necessary resources for performing operations.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.users import User
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.app.services.uow.sqlalchemy import SqlAlchemyUnitOfWork
from src.app.services.users import get_user_by_email
from src.auth.services import decode_token_data
from src.database import get_session_depend

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_uow(session: AsyncSession = Depends(get_session_depend)) -> AbstractUnitOfWork:
    """
    :param session: database session
    :return: UnitOfWork
    """
    yield SqlAlchemyUnitOfWork(session)


async def get_current_user(
    uow: AbstractUnitOfWork = Depends(get_uow), token: str = Depends(oauth2_scheme)
) -> User:
    """
    FastApi dependency to retrieve a user based on JWT (JSON Web Token)
    :return: User
    """
    token_data = decode_token_data(token)
    if token_data is None:
        raise_credentials_exception()
    return await get_user_by_email(uow, token_data.email)


def raise_credentials_exception():
    """
    Raises HTTPException.
    Called when the JWT passed in the headers is invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    raise credentials_exception
