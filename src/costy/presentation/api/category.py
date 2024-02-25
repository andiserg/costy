from litestar import Controller, get, post

from costy.application.category.dto import NewCategoryDTO
from costy.application.common.id_provider import IdProvider
from costy.domain.models.category import Category, CategoryId
from costy.presentation.interactor_factory import InteractorFactory


class CategoryController(Controller):
    path = '/categories'

    @get()
    async def get_list_categories(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
    ) -> list[Category]:
        async with ioc.read_available_categories(
            id_provider
        ) as read_available_categories:
            return await read_available_categories()

    @post()
    async def create_operation(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        data: NewCategoryDTO,
    ) -> CategoryId:
        async with ioc.create_category(id_provider) as create_category:
            return await create_category(data)
