from typing import Protocol

from costy.application.category.dto import UpdateCategoryDTO
from costy.application.common.category_gateway import (
    CategoryReader,
    CategoryUpdater,
)
from costy.application.common.id_provider import IdProvider
from costy.application.common.interactor import Interactor
from costy.application.common.uow import UoW
from costy.domain.exceptions.access import AccessDeniedError
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.services.access import AccessService
from costy.domain.services.category import CategoryService


class CategoryGateway(CategoryReader, CategoryUpdater, Protocol):
    ...


class UpdateCategory(Interactor[UpdateCategoryDTO, None]):
    def __init__(
        self,
        category_service: CategoryService,
        access_service: AccessService,
        category_db_gateway: CategoryGateway,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.category_service = category_service
        self.access_service = access_service
        self.category_db_gateway = category_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: UpdateCategoryDTO) -> None:
        user_id = await self.id_provider.get_current_user_id()
        category = await self.category_db_gateway.get_category(data.category_id)

        if not category or not category.id:
            raise InvalidRequestError("Category not exist")

        if not self.access_service.ensure_can_edit(category, user_id):
            raise AccessDeniedError("User can't edit this operation.")

        self.category_service.update(category, data.data.name)
        await self.category_db_gateway.update_category(category.id, category)
        await self.uow.commit()
