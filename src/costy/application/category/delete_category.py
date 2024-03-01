from costy.application.common.category_gateway import CategoryDeleter
from costy.application.common.id_provider import IdProvider
from costy.application.common.interactor import Interactor
from costy.application.common.uow import UoW
from costy.domain.models.category import CategoryId


class DeleteCategory(Interactor[CategoryId, None]):
    def __init__(
        self,
        category_gateway: CategoryDeleter,
        id_provider: IdProvider,
        uow: UoW
    ):
        self.category_gateway = category_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, category_id: CategoryId) -> None:
        # user_id = await self.id_provider.get_current_user_id()  # type: ignore

        # TODO: Add check that user is owner of category
        await self.category_gateway.delete_category(category_id)
        await self.uow.commit()
