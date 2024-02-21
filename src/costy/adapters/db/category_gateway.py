from adaptix import Retort
from sqlalchemy import Table, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.category.dto import CategoryDTO
from costy.application.common.category_gateway import (
    CategoriesReader,
    CategoryDeleter,
    CategoryReader,
    CategorySaver,
)
from costy.domain.models.category import Category, CategoryId
from costy.domain.models.user import UserId


class CategoryGateway(
    CategoryReader, CategorySaver, CategoryDeleter, CategoriesReader
):
    def __init__(self, session: AsyncSession, table: Table, retort: Retort):
        self.session = session
        self.table = table
        self.retort = retort

    async def get_category(self, category_id: CategoryId) -> Category | None:
        query = select(self.table).where(
            self.table.c.id == category_id
        )
        result: Category | None = await self.session.scalar(query)
        return result

    async def save_category(self, category: Category) -> None:
        self.session.add(category)
        await self.session.flush(objects=[category])

    async def delete_category(self, category_id: CategoryId) -> None:
        query = delete(Category).where(
            self.table.c.id == category_id
        )
        await self.session.execute(query)

    async def find_categories(self, user_id: UserId) -> list[CategoryDTO]:
        filter_expr = or_(
            self.table.c.user_id == user_id,
            self.table.c.user_id == None  # noqa: E711
        )
        query = select(self.table).where(filter_expr)
        categories = list(await self.session.scalars(query))
        dumped = self.retort.dump(categories, list[Category])
        return self.retort.load(dumped, list[CategoryDTO])
