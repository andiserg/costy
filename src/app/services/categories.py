from src.app.domain.categories import Category
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.schemas.categories import CategoryCreateSchema


async def create_category(
    uow: AbstractUnitOfWork, user_id: int, schema: CategoryCreateSchema
) -> Category:
    async with uow:
        created_category = await uow.categories.get(name=schema.name, user_id=user_id)
        if created_category:
            return created_category
        category = Category(name=schema.name, user_id=user_id)
        await uow.categories.add(category)
        await uow.commit()
        return category


async def get_availables_categories(
    uow: AbstractUnitOfWork, user_id: int
) -> list[Category]:
    async with uow:
        return await uow.categories.get_availables(user_id)
