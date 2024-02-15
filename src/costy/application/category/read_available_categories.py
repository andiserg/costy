from typing import List, Optional

from costy.domain.services.category import CategoryService

from ..common.category_gateway import CategoriesReader
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.uow import UoW
from .dto import CategoryDTO, ReadAvailableCategoriesDTO


class ReadAvailableCategories(Interactor[None, List[CategoryDTO]]):
    def __init__(
        self,
        category_service: CategoryService,
        category_db_gateway: CategoriesReader,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.category_service = category_service
        self.category_db_gateway = category_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(
        self, data: Optional[ReadAvailableCategoriesDTO] = None
    ) -> List[CategoryDTO]:
        user_id = await self.id_provider.get_current_user_id()
        return await self.category_db_gateway.find_categories(user_id)  # type: ignore
