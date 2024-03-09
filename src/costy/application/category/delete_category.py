from typing import Protocol

from ...domain.exceptions.access import AccessDeniedError
from ...domain.exceptions.base import InvalidRequestError
from ...domain.models.category import CategoryId
from ...domain.services.access import AccessService
from ..common.category_gateway import CategoryDeleter, CategoryReader
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.uow import UoW


class CategoryGateway(CategoryReader, CategoryDeleter, Protocol):
    ...


class DeleteCategory(Interactor[CategoryId, None]):
    def __init__(
        self,
        access_service: AccessService,
        category_gateway: CategoryGateway,
        id_provider: IdProvider,
        uow: UoW
    ):
        self.access_service = access_service
        self.category_gateway = category_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, category_id: CategoryId) -> None:
        user_id = await self.id_provider.get_current_user_id()
        category = await self.category_gateway.get_category(category_id)

        if not category:
            raise InvalidRequestError("Category not exist")

        if not self.access_service.ensure_can_edit(category, user_id):
            raise AccessDeniedError("User does not have permission to delete this category")

        await self.category_gateway.delete_category(category_id)
        await self.uow.commit()
