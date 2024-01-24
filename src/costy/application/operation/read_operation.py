from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.operation_gateway import OperationReader
from ..common.uow import UoW
from costy.domain.models.operation import OperationId, Operation
from costy.domain.services.operation import OperationService


class ReadOperation(Interactor[OperationId, Operation]):
    def __init__(
        self,
        operation_service: OperationService,
        operation_db_gateway: OperationReader,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.operation_service = operation_service
        self.operation_db_gateway = operation_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, operation_id: OperationId):
        user_id = await self.id_provider.get_current_user_id()

        operation = await self.operation_db_gateway.get_operation(operation_id)

        # TODO: Move to access service
        if operation.user_id != user_id:
            raise Exception("User must be the owner of the operation")

        return operation
