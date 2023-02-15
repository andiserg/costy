"""
users methods test
"""
import pytest

from app.apps.account.users.models import User
from app.apps.account.users.schemas import UserCreateSchema
from app.apps.account.users.services import create_user, get_user, get_user_by_email

# event_loop, database потрібні для правильного функціонування тестів
from app.tests.config import database, event_loop, precents_evn_variables  # noqa: F401;


@pytest.mark.asyncio
@precents_evn_variables
async def test_user_create(database):  # noqa: F401, F811;
    """
    Перевірка методу app.crud.users.create_user
    create_user повинен зберегти об'єкт User в БД та повернути його
    """
    user_schema = UserCreateSchema(  # nosec B106
        email="test@test.com", password="123456"
    )
    async with database.sessionmaker() as session:
        result = await create_user(session, user_schema)
        assert isinstance(result, User)


@pytest.mark.asyncio
@precents_evn_variables
async def test_user_read(database):  # noqa: F401, F811;
    """
    Перевірка методів
        app.crud.users.get_user
        app.crud.users.get_user_by_email
    """
    user_schema = UserCreateSchema(  # nosec B106
        email="test@test.com", password="123456"
    )
    async with database.sessionmaker() as session:
        # Створення користувача
        created_user: User = await create_user(session, user_schema)

        # Запит існуючого користувача по ID
        user = await get_user(session, created_user.id)
        assert isinstance(user, User)
        assert user.email == created_user.email

        # Запит існуючого користувача по ID
        user = await get_user_by_email(session, created_user.email)
        assert isinstance(user, User)
        assert user.email == created_user.email

        # Запит неіснуючого користувача по ID
        user = await get_user(session, 9999)
        assert user is None

        # Запит неіснуючого користувача по ID
        user = await get_user_by_email(session, "incorrect@test.com")
        assert user is None
