"""
users methods test
"""
import pytest

from src.app.account.users.models import User
from src.app.account.users.services import create_user
from src.app.adapters.repository import UserRepository
from src.app.unit_of_work import SqlAlchemyUnitOfWork
from src.schemas.users import UserCreateSchema

# event_loop, database потрібні для правильного функціонування тестів
from tests.config import database, event_loop, precents_evn_variables  # noqa: F401;


@pytest.mark.asyncio
@precents_evn_variables
async def test_user_create(database):  # noqa: F401, F811;
    """
    Перевірка методу src.crud.users.create_user
    create_user повинен зберегти об'єкт User в БД та повернути його
    """
    user_schema = UserCreateSchema(  # nosec B106
        email="test@test.com", password="123456"
    )
    async with database.sessionmaker() as session:
        uow = SqlAlchemyUnitOfWork(session)
        result = await create_user(uow, user_schema)
        assert isinstance(result, User)


@pytest.mark.asyncio
@precents_evn_variables
async def test_user_read(database):  # noqa: F401, F811;
    """
    Перевірка методів
        src.crud.users.get_user
        src.crud.users.get_user_by_email
    """
    user_schema = UserCreateSchema(  # nosec B106
        email="test@test.com", password="123456"
    )
    async with database.sessionmaker() as session:
        uow = SqlAlchemyUnitOfWork(session)
        users = UserRepository(session)

        # Створення користувача
        created_user: User = await create_user(uow, user_schema)

        # Запит існуючого користувача по ID
        user = await users.get("id", created_user.id)
        assert isinstance(user, User)
        assert user.email == created_user.email

        # Запит існуючого користувача по ID
        user = await users.get("email", created_user.email)
        assert isinstance(user, User)
        assert user.email == created_user.email

        # Запит неіснуючого користувача по ID
        user = await users.get("id", 9999)
        assert user is None

        # Запит неіснуючого користувача по ID
        user = await users.get("email", "incorrect@test.com")
        assert user is None
