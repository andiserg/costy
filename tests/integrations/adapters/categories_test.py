from random import choices
from string import ascii_lowercase, digits

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.categories import Category
from src.app.repositories.categories import CategoryRepository
from tests.patterns import create_user_with_orm


async def create_categories(session: AsyncSession, num=10, user_id=None, type="system"):
    for i in range(num):
        session.add(
            Category(
                name=f"Test {type} category #{i}-{''.join(choices(ascii_lowercase + digits, k=5))}",
                user_id=user_id,
                type=type,
            )
        )
    await session.commit()


@pytest.mark.asyncio
async def test_create_and_read_categories(database):
    async with database.sessionmaker() as session:
        repository = CategoryRepository(session)
        created_user = await create_user_with_orm(session)
        await create_categories(session, num=10, user_id=created_user.id, type="user")

        await repository.add(
            Category(name=f"Test common category", user_id=None, type="system")
        )
        await session.commit()

        categories = await repository.get_availables(created_user.id)
        assert len(categories) == 11


@pytest.mark.asyncio
async def test_read_categories_in_id_list(database):
    async with database.sessionmaker() as session:
        repository = CategoryRepository(session)
        created_user = await create_user_with_orm(session)
        await create_categories(session, num=10, user_id=created_user.id, type="user")
        categories = await repository.get_categories_in_values(
            "id", [6, 7, 8, 9, 10, 11]
        )
        # Створено лише 10 категорій, до 10 id.
        # 11 id немає, тому повинно бути повернено 5 категорій.
        assert len(categories) == 5
