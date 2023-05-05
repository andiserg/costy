"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.app.services.uow.abstract import AbstractUnitOfWork
from src.app.services.users import get_user_by_email
from src.auth.password import verify_password
from src.auth.services import create_access_token
from src.depends import get_uow
from src.schemas.auth import Token

router = APIRouter()


@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Логін користувача за допомогою формування JWT.
    Якщо дані для входу не вірні - піднімається помилка

    :param uow: Unit of Work
    :param form_data: схема, яка формується на базі введених даних користувача.
    :return: jwt і тип токену. Для використання потрібно вказати як header у вигляді

        Authorization: <token_type> <access_token>

    """
    user = await get_user_by_email(uow, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
