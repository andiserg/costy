from dataclasses import dataclass, field

from dishka import AsyncContainer, FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, put, Request

from costy.application.category.create_category import CreateCategory
from costy.application.category.delete_category import DeleteCategory
from costy.application.category.read_available_categories import ReadAvailableCategories
from costy.application.category.update_category import UpdateCategory
from costy.application.common.category.dto import NewCategoryDTO, UpdateCategoryData, UpdateCategoryDTO
from costy.application.common.id_provider import IdProvider
from costy.domain.models.category import Category, CategoryId
from costy.domain.sentinel import Sentinel


@dataclass(slots=True, kw_only=True)
class UpdateCategoryPureData:
    name: str | None = None
    view: dict | None = field(default_factory=dict)


class CategoryController(Controller):
    path = "/categories"
    tags = ("Categories",)

    @get()
    @inject
    async def get_list_categories(
        self,
        read_available_categories: FromDishka[ReadAvailableCategories]
    ) -> list[Category]:
        return await read_available_categories()

    @post()
    @inject
    async def create_category(
        self,
        create_category: FromDishka[CreateCategory],
        data: NewCategoryDTO,
    ) -> CategoryId:
        return await create_category(data)

    @delete("{category_id:int}")
    @inject
    async def delete_category(
        self,
        category_id: int,
        delete_category: FromDishka[DeleteCategory]
    ) -> None:
        await delete_category(CategoryId(category_id))

    @put("{category_id:int}")
    @inject
    async def update_category(
        self,
        category_id: int,
        update_category: FromDishka[UpdateCategory],
        data: UpdateCategoryPureData,
    ) -> None:
        input_data = UpdateCategoryDTO(
            CategoryId(category_id),
            UpdateCategoryData(
                name=data.name,
                view=data.view if data.view != {} else Sentinel,
            ),
        )
        await update_category(input_data)
