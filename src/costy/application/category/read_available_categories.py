from dataclasses import dataclass
from typing import List, Optional

from costy.domain.models.category import CategoryId, CategoryType
from costy.domain.services.category import CategoryService

from ..common.category_gateway import CategoriesReader
from ..common.converter import Converter
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.uow import UoW


@dataclass
class ReadAvailableCategoriesDTO:
    ...


@dataclass
class CategoryDTO:
    id: CategoryId | None
    name: str
    kind: CategoryType


class ReadAvailableCategories(Interactor[None, List[CategoryDTO]]):
    def __init__(
        self,
        category_service: CategoryService,
        category_db_gateway: CategoriesReader,
        converter: Converter,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.category_service = category_service
        self.category_db_gateway = category_db_gateway
        self.converter = converter
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(
        self, data: Optional[ReadAvailableCategoriesDTO] = None
    ) -> List[CategoryDTO]:
        user_id = await self.id_provider.get_current_user_id()
        categories = await self.category_db_gateway.find_categories(user_id)
        return self.converter.convert(categories, list[CategoryDTO])
