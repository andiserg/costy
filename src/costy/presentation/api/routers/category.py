from dataclasses import dataclass, field

from litestar import Controller, delete, get, post, put

from costy.application.common.category.dto import (
    NewCategoryDTO,
    UpdateCategoryData,
    UpdateCategoryDTO,
)
from costy.application.common.id_provider import IdProvider
from costy.domain.models.category import Category, CategoryId
from costy.domain.sentinel import Sentinel
from costy.presentation.interactor_factory import InteractorFactory


@dataclass(slots=True, kw_only=True)
class UpdateCategoryPureData:
    name: str | None = None
    view: dict | None = field(default_factory=dict)


class CategoryController(Controller):
    path = '/categories'
    tags = ("Categories",)

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
    async def create_category(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        data: NewCategoryDTO,
    ) -> CategoryId:
        async with ioc.create_category(id_provider) as create_category:
            return await create_category(data)

    @delete("{category_id:int}")
    async def delete_category(
        self,
        category_id: int,
        ioc: InteractorFactory,
        id_provider: IdProvider,
    ) -> None:
        async with ioc.delete_category(id_provider) as delete_category:
            await delete_category(CategoryId(category_id))

    @put("{category_id:int}")
    async def update_category(
        self,
        category_id: int,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        data: UpdateCategoryPureData,
    ) -> None:
        async with ioc.update_category(id_provider) as update_category:
            input_data = UpdateCategoryDTO(
                CategoryId(category_id),
                UpdateCategoryData(
                    name=data.name,
                    view=data.view if data.view != {} else Sentinel
                )
            )
            await update_category(input_data)
