from litestar import Controller, get

from costy.application.category.dto import CategoryDTO
from costy.application.common.id_provider import IdProvider
from costy.presentation.interactor_factory import InteractorFactory


class CategoryController(Controller):
    path = '/categories'

    @get()
    async def get_list_categories(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
    ) -> list[CategoryDTO]:
        async with ioc.read_available_categories(
            id_provider
        ) as read_available_categories:
            return await read_available_categories()
