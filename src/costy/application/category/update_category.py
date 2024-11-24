from dataclasses import dataclass
from typing import Protocol

from ...domain.exceptions.access import AccessDeniedError
from ...domain.exceptions.base import InvalidRequestError
from ...domain.models.category import CategoryId
from ...domain.sentinel import Sentinel, SentinelOptional
from ...domain.services.access import AccessService
from ...domain.services.category import CategoryService
from ..common.category_gateway import CategoryReader, CategoryUpdater
from ..common.commiter import Commiter
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor


class CategoryGateway(CategoryReader, CategoryUpdater, Protocol):
    ...


@dataclass(slots=True, kw_only=True)
class UpdateCategoryData:
    name: str | None = None
    view: SentinelOptional[dict[str, str]] = Sentinel


@dataclass
class InputData:
    category_id: CategoryId
    data: UpdateCategoryData


class UpdateCategory(Interactor[InputData, None]):
    def __init__(
        self,
        category_service: CategoryService,
        access_service: AccessService,
        category_db_gateway: CategoryGateway,
        id_provider: IdProvider,
        uow: Commiter,
    ) -> None:
        self.category_service = category_service
        self.access_service = access_service
        self.category_db_gateway = category_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: InputData) -> None:
        user_id = await self.id_provider.get_current_user_id()
        category = await self.category_db_gateway.get_category_by_id(data.category_id)

        if not category or not category.id:
            raise InvalidRequestError("Category not exist")

        if not self.access_service.ensure_can_edit(category, user_id):
            raise AccessDeniedError("User can't edit this category.")

        self.category_service.update(category, data.data.name, data.data.view)
        await self.category_db_gateway.update_category(category.id, category)
        await self.uow.commit()
