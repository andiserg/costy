from src.app.domain.categories import Category
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.schemas.categories import CategoryCreateSchema


async def create_category(
    uow: AbstractUnitOfWork, user_id: int, schema: CategoryCreateSchema
) -> Category:
    async with uow:
        category = Category(
            name=schema.name,
            user_id=user_id,
            type="user",
            icon_name=schema.icon_name,
            icon_color=schema.icon_color.upper(),
        )
        await uow.categories.add(category)
        await uow.commit()
        return category


async def get_availables_categories(
    uow: AbstractUnitOfWork, user_id: int
) -> list[Category]:
    async with uow:
        return await uow.categories.get_availables(user_id)


async def get_categories_in_values(
    uow: AbstractUnitOfWork, field: str, values: list
) -> list[Category]:
    async with uow:
        return await uow.categories.get_categories_in_values(field, values)


async def delete_category(
    uow: AbstractUnitOfWork, user_id: int, category_id: int
) -> bool:
    async with uow:
        category = await uow.categories.get(
            id=category_id, user_id=user_id, type="user"
        )
        if category:
            await uow.operations.delete(category_id=category_id)
            await uow.limits.delete(category_id=category_id)
            await uow.categories.delete(category_id=category_id)
            await uow.commit()
            return True
        return False
