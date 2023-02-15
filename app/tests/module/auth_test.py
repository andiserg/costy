"""
Auth module tests
"""
import pytest

from app.account.auth.services import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.account.users.models import User
from app.account.users.schemas import UserCreateSchema
from app.account.users.services import create_user
from app.tests.config import database  # noqa: F401;


@pytest.mark.asyncio
async def test_auth_user(database):  # noqa: F811;
    """
    Testing user account func
    authenticate_user(email, password) ->
        User: якщо email є в базі і password сходиться
        None: якщо email немає в базі або password не сходиться
    """
    user_schema = UserCreateSchema(email="test", password="test")  # nosec B106
    async with database.sessionmaker() as session:
        created_user = await create_user(session, user_schema)

        # Перевірка з правильним даними
        correct_auth = await authenticate_user(
            session, user_schema.email, user_schema.password
        )
        assert isinstance(correct_auth, User)
        assert created_user.email == correct_auth.email

        # Перевірка з неправильним email
        incorrect_email_auth = await authenticate_user(
            session, "incorrect", user_schema.password
        )
        assert incorrect_email_auth is None

        # Перевірка з неправильним password
        incorrect_password_auth = await authenticate_user(
            session, user_schema.email, "incorrect"
        )
        assert incorrect_password_auth is None

        # Перевірка з неправильним email & password
        incorrect_email_password_auth = await authenticate_user(
            session, "incorrect", "incorrect"
        )
        assert incorrect_email_password_auth is None


@pytest.mark.asyncio
async def test_jwt_work(database):  # noqa: F811;
    """
    Тест роботи методів, які використовують JWT.
    Шифрує інформацію про користувача у JWT, потім його розшифровує.
    Якщо на виході отриманий той самий користувач що був на вході - test passed.
    """
    async with database.sessionmaker() as session:
        user_schema = UserCreateSchema(email="test", password="test")  # nosec B106
        created_user = await create_user(session, user_schema)

        token = create_access_token({"sub": created_user.email})
        decode_user = await get_current_user(session, token)
        assert isinstance(decode_user, User)
        assert decode_user.id == created_user.id

        # Спроба розшифрувати неправильний токен. Результат повинен бути None
        decode_result = await get_current_user(session, "incorrect")
        assert decode_result is None
