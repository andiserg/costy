from adaptix import Retort
from sqlalchemy import Table, delete, insert, join, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.category.category_gateway import (
    CategoriesFinder,
    CategoriesReader,
    CategoryDeleter,
    CategoryFinder,
    CategoryReader,
    CategorySaver,
    CategoryUpdater,
    SentinelOptional,
)
from costy.domain.models.category import Category, CategoryId
from costy.domain.models.user import UserId
from costy.domain.sentinel import Sentinel


class CategoryGateway(
    CategoryReader,
    CategoryFinder,
    CategorySaver,
    CategoryDeleter,
    CategoriesReader,
    CategoryUpdater,
    CategoriesFinder
):
    def __init__(self, session: AsyncSession, category_table: Table, mcc_table: Table, retort: Retort):
        self.session = session
        self.category_table = category_table
        self.mcc_table = mcc_table
        self.retort = retort

    async def get_category_by_id(self, category_id: CategoryId) -> Category | None:
        query = select(self.category_table).where(self.category_table.c.id == category_id)
        result = await self.session.execute(query)
        data = next(result.mappings(), None)
        return self.retort.load(data, Category) if data else None

    async def find_category(
        self,
        name: SentinelOptional[str] = Sentinel,
        kind: SentinelOptional[str] = Sentinel,
        user_id: SentinelOptional[UserId] = Sentinel
    ) -> Category | None:
        if not any(param is not Sentinel for param in (name, kind, user_id)):
            return None

        params = {
            "name": name,
            "kind": kind,
            "user_id": user_id
        }

        stmt = select(self.category_table)
        for param_name, param_value in params.items():
            if param_value is not Sentinel:
                stmt = stmt.where(self.category_table.c[param_name] == param_value)

        result = (await self.session.execute(stmt)).fetchone()
        return self.retort.load(result._mapping, Category)

    async def save_category(self, category: Category) -> None:
        values = self.retort.dump(category)
        del values["id"]
        query = insert(self.category_table).values(**values)
        result = await self.session.execute(query)
        category.id = CategoryId(result.inserted_primary_key[0])

    async def delete_category(self, category_id: CategoryId) -> None:
        query = delete(self.category_table).where(self.category_table.c.id == category_id)
        await self.session.execute(query)

    async def find_categories(self, user_id: UserId) -> list[Category]:
        filter_expr = or_(
            self.category_table.c.user_id == user_id,
            self.category_table.c.user_id == None  # noqa: E711
        )
        query = select(self.category_table).where(filter_expr)
        result = await self.session.execute(query)
        return self.retort.load(result.mappings(), list[Category])

    async def update_category(self, category_id: CategoryId, category: Category) -> None:
        values = self.retort.dump(category)

        if not values:
            return

        query = update(self.category_table).where(self.category_table.c.id == category_id).values(**values)
        await self.session.execute(query)

    async def find_categories_by_mcc_codes(self, mcc_codes: tuple[int, ...]) -> dict[int, Category]:
        j = join(self.mcc_table, self.category_table)
        stmt = (
            select(self.mcc_table, self.category_table)
            .where(self.mcc_table.c.mcc.in_(mcc_codes))
            .select_from(j)
        )
        result = tuple((await self.session.execute(stmt)).mappings())

        if not result:
            return {}

        category_map = {item["mcc"]: item for item in result}
        return self.retort.load(category_map, dict[int, Category])
