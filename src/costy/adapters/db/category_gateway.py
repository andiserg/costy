from adaptix import Retort
from sqlalchemy import delete, or_, select
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
    def __init__(self, session: AsyncSession, retort: Retort):
        self.session = session
        self.retort = retort

    async def get_category(self, category_id: CategoryId) -> Category | None:
        query = select(Category).where(
            Category.id == category_id  # type: ignore
        )
        result: Category | None = await self.session.scalar(query)
        return result

    async def save_category(self, category: Category) -> None:
        self.session.add(category)
        await self.session.flush(objects=[category])

    async def delete_category(self, category_id: CategoryId) -> None:
        query = delete(Category).where(
            Category.id == category_id  # type: ignore
        )
        await self.session.execute(query)

    async def find_categories(self, user_id: UserId) -> list[CategoryDTO]:
        filter_expr = or_(
            Category.user_id == user_id,  # type: ignore
            Category.user_id == None  # type: ignore # noqa: E711
        )
        query = select(Category).where(filter_expr)
        categories = list(await self.session.scalars(query))
        dumped = self.retort.dump(categories, list[Category])
        return self.retort.load(dumped, list[CategoryDTO])
