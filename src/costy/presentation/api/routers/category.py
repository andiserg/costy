from dataclasses import dataclass, field

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, put

from costy.application.category import (
    create_category,
    delete_category,
    read_available_categories,
    update_category,
)
from costy.domain.models.category import Category, CategoryId
from costy.domain.sentinel import Sentinel


@dataclass(slots=True, kw_only=True)
class UpdateCategoryPureData:
    name: str | None = None
    view: dict[str, str] | None = field(default_factory=dict)


class CategoryController(Controller):
    path = "/categories"
    tags = ("Categories",)

    @get()
    @inject
    async def get_list_categories(
        self,
        service: FromDishka[read_available_categories.ReadAvailableCategories],
    ) -> list[Category]:
        return await service(None)

    @post()
    @inject
    async def create_category(
        self,
        service: FromDishka[create_category.CreateCategory],
        data: create_category.InputData,
    ) -> CategoryId:
        return await service(data)

    @delete("{category_id:int}")
    @inject
    async def delete_category(
        self,
        category_id: int,
        service: FromDishka[delete_category.DeleteCategory],
    ) -> None:
        await service(CategoryId(category_id))

    @put("{category_id:int}")
    @inject
    async def update_category(
        self,
        category_id: int,
        service: FromDishka[update_category.UpdateCategory],
        data: UpdateCategoryPureData,
    ) -> None:
        input_data = update_category.InputData(
            CategoryId(category_id),
            update_category.UpdateCategoryData(
                name=data.name,
                view=data.view if data.view != {} else Sentinel,
            ),
        )
        await service(input_data)
