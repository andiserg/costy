from src.app.domain.categories import Category
from src.app.repositories.absctract.categories import ACategoryRepository
from tests.fake_adapters.base import FakeRepository


class FakeCategoryRepository(FakeRepository, ACategoryRepository):
    async def delete(self, category_id: int):
        pass

    async def get(self, **kwargs) -> Category | None:
        return await self._get(**kwargs)

    async def _get_categories(self, *args) -> list[Category]:
        pass

    async def get_availables(self, user_id) -> list[Category]:
        return list(
            filter(
                lambda category: category.user_id == user_id
                or category.user_id is None,
                self.instances,
            )
        )

    async def get_categories_in_values(
        self, field: str, values: list
    ) -> list[Category]:
        return list(
            filter(
                lambda category: category.__dict__.get(field) in values, self.instances
            )
        )
