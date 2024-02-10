from typing import List

from costy.domain.models.operation import Operation
from costy.domain.services.operation import OperationService

from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.operation_gateway import OperationsReader
from ..common.uow import UoW
from .dto import ListOperationDTO


class ReadListOperation(Interactor[ListOperationDTO, List[Operation]]):
    def __init__(
        self,
        operation_service: OperationService,
        operation_db_gateway: OperationsReader,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.operation_service = operation_service
        self.operation_db_gateway = operation_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: ListOperationDTO) -> List[Operation]:
        user_id = await self.id_provider.get_current_user_id()

        operations = await self.operation_db_gateway.find_operations_by_user(
            user_id,
            data.from_time,
            data.to_time,
        )

        return operations
