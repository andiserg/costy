import json
import os

from sqlalchemy import or_, select

from src.app.domain.categories import Category
from src.app.repositories.absctract.categories import ACategoryRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class CategoryRepository(SqlAlchemyRepository, ACategoryRepository):
    async def get(self, **kwargs) -> Category:
        return await self._get(Category, **kwargs)

    async def _get_categories(self, *args) -> list[Category]:
        return list(await self.session.scalars(select(Category).filter(*args)))

    async def get_availables(self, user_id) -> list[Category]:
        return await self._get_categories(
            or_(Category.user_id == user_id, Category.user_id == None)  # noqa: E711
        )

    async def get_categories_in_values(
        self, field: str, values: list
    ) -> list[Category]:
        return await self._get_categories(Category.__dict__.get(field).in_(values))


class CategoryMccFacade:
    @staticmethod
    def get_category_name_by_mcc(mcc: int):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "mcc.json")
        with open(filename, encoding="utf-8") as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                if mcc in value:
                    return key
