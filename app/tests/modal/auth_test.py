"""
Auth modal tests
"""
import pytest

from app.crud.auth import authenticate_user
from app.crud.users import create_user
from app.models.users import User
from app.schemas.users import UserCreateSchema
from app.tests.config import database  # noqa: F401;


@pytest.mark.asyncio
async def test_auth_user(database):  # noqa: F811;
    """
    Testing user auth func
    authenticate_user(email, password) ->
        User: якщо email є в базі і password сходиться
        None: якщо email немає в базі або password не сходиться
    """
    user_schema = UserCreateSchema(email="test", password="test")  # nosec B106
    async with database.sessionmaker() as session:
        created_user = await create_user(session, user_schema)

        # Перевірка з правильним даними
        correct_auth = await authenticate_user(
            user_schema.email, user_schema.password, session
        )
        assert isinstance(correct_auth, User)
        assert created_user.email == correct_auth.email

        # Перевірка з неправильним email
        incorrect_email_auth = await authenticate_user(
            "incorrect", user_schema.password, session
        )
        assert incorrect_email_auth is None

        # Перевірка з неправильним password
        incorrect_password_auth = await authenticate_user(
            user_schema.email, "incorrect", session
        )
        assert incorrect_password_auth is None

        # Перевірка з неправильним email & password
        incorrect_password_auth = await authenticate_user(
            "incorrect", "incorrect", session
        )
        assert incorrect_password_auth is None
