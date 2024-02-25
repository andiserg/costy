from adaptix import Retort
from sqlalchemy import Table, delete, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

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
        query = select(self.table).where(self.table.c.id == category_id)
        result = await self.session.execute(query)
        data = next(result.mappings(), None)
        return self.retort.load(data, Category) if data else None

    async def save_category(self, category: Category) -> None:
        values = self.retort.dump(category)
        del values["id"]
        query = insert(self.table).values(**values)
        result = await self.session.execute(query)
        category.id = CategoryId(result.inserted_primary_key[0])

    async def delete_category(self, category_id: CategoryId) -> None:
        query = delete(self.table).where(self.table.c.id == category_id)
        await self.session.execute(query)

    async def find_categories(self, user_id: UserId) -> list[Category]:
        filter_expr = or_(
            self.table.c.user_id == user_id,
            self.table.c.user_id == None  # noqa: E711
        )
        query = select(self.table).where(filter_expr)
        result = await self.session.execute(query)
        return self.retort.load(result.mappings(), list[Category])
