from src.app.domain.categories import Category
from src.app.repositories.absctract.categories import ACategoryRepository
from tests.fake_adapters.base import FakeRepository


class FakeCategoryRepository(FakeRepository, ACategoryRepository):
    async def get(self, prop, value) -> Category | None:
        return await self._get(prop, value)

    async def get_availables(self, user_id) -> list[Category]:
        return list(
            filter(
                lambda category: category.user_id == user_id
                or category.user_id is None,
                self.instances,
            )
        )
