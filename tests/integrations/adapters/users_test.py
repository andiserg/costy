import pytest

from src.app.domain.users import User
from src.app.repositories.users import UserRepository
from tests.conftest import precents_env_variables


@pytest.mark.asyncio
@precents_env_variables
async def test_create_and_read_user_by_all_fields(database):
    async with database.sessionmaker() as session:
        user = User(email="test", hashed_password="fake_hashed_password")
        repository = UserRepository(session)
        await repository.add(user)
        await session.commit()

        results = [
            await repository.get("id", user.id),
            await repository.get("email", user.email),
        ]
        assert all(results)


@pytest.mark.asyncio
async def test_read_user_with_incorrect_data(database):
    async with database.sessionmaker() as session:
        repository = UserRepository(session)
        assert await repository.get("id", 100000) is None
        assert await repository.get("email", "incorrect") is None
