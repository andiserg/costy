from sqlalchemy import or_, select

from src.app.domain.categories import Category
from src.app.repositories.absctract.categories import ACategoryRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class CategoryRepository(SqlAlchemyRepository, ACategoryRepository):
    async def get(self, **kwargs) -> Category:
        return await self._get(Category, **kwargs)

    async def get_categories(self, *args) -> list[Category]:
        return list(await self.session.scalars(select(Category).filter(*args)))

    async def get_availables(self, user_id) -> list[Category]:
        return list(
            await self.get_categories(
                or_(Category.user_id == user_id, Category.user_id == None)  # noqa: E711
            )
        )