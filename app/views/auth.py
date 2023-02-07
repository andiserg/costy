"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth import authenticate_user, create_access_token
from app.main import get_session
from app.schemas.auth import Token

router = APIRouter()


@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """
    Логін користувача за допомогою формування JWT.
    Якщо дані для входу не вірні - піднімається помилка

    :param form_data: схема, яка формується на базі введених даних користувача.
    :param session: сесія DB.
    :return: jwt і тип токену. Для використання потрібно вказати як header у вигляді

        Authorization: <token_type> <access_token>

    """
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
