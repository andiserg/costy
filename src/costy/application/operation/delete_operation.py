from costy.application.common.id_provider import IdProvider
from costy.application.common.interactor import Interactor
from costy.application.common.operation_gateway import OperationDeleter
from costy.application.common.uow import UoW
from costy.domain.models.operation import OperationId


class DeleteOperation(Interactor[OperationId, None]):
    def __init__(
        self,
        operation_gateway: OperationDeleter,
        id_provider: IdProvider,
        uow: UoW
    ):
        self.operation_gateway = operation_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, operation_id: OperationId) -> None:
        # user_id = await self.id_provider.get_current_user_id()  # type: ignore

        # TODO: Add check that user is owner of operation
        await self.operation_gateway.delete_operation(operation_id)
        await self.uow.commit()
