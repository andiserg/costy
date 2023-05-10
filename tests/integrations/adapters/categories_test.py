import pytest

from src.app.domain.categories import Category
from src.app.repositories.categories import CategoryRepository
from tests.patterns import create_user_with_orm


@pytest.mark.asyncio
async def test_create_and_read_categories(database):
    async with database.sessionmaker() as session:
        repository = CategoryRepository(session)
        created_user = await create_user_with_orm(session)
        for i in range(10):
            await repository.add(
                Category(
                    name=f"Test category #{i}",
                    user_id=created_user.id,
                )
            )
        await repository.add(
            Category(
                name=f"Test common category",
                user_id=None,
            )
        )
        await session.commit()

        categories = await repository.get_availables(created_user.id)
        assert len(categories) == 11
