from costy.application.common.category.category_gateway import CategorySaver
from costy.application.common.category.dto import NewCategoryDTO
from costy.domain.models.category import CategoryId, CategoryType
from costy.domain.services.category import CategoryService

from ...domain.exceptions.access import AuthenticationError
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.uow import UoW


class CreateCategory(Interactor[NewCategoryDTO, CategoryId]):
    def __init__(
        self,
        category_service: CategoryService,
        category_db_gateway: CategorySaver,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.category_service = category_service
        self.category_db_gateway = category_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: NewCategoryDTO) -> CategoryId:
        user_id = await self.id_provider.get_current_user_id()

        if not user_id:
            raise AuthenticationError("User not found")

        category = self.category_service.create(data.name, CategoryType.PERSONAL, user_id)
        await self.category_db_gateway.save_category(category)
        category_id = category.id
        await self.uow.commit()
        return category_id  # type: ignore
