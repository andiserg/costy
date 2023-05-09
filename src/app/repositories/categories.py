from sqlalchemy import or_, select

from src.app.domain.categories import Category
from src.app.repositories.absctract.categories import ACategoryRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class CategoryRepository(SqlAlchemyRepository, ACategoryRepository):
    async def get(self, field, value) -> Category:
        return await self._get(Category, field, value)

    async def get_availables(self, user_id) -> list[Category]:
        return list(
            await self.session.scalars(
                select(Category).filter(
                    or_(
                        Category.user_id == user_id,
                        Category.user_id == None,  # noqa: E711
                    )
                )
            )
        )
