from dataclasses import dataclass

from ...domain.models.operation import Operation
from ...domain.services.operation import OperationService
from ..common.commiter import Commiter
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.operation_gateway import OperationsReader


@dataclass(slots=True)
class InputData:
    from_time: int | None = None
    to_time: int | None = None


class ReadListOperation(Interactor[InputData, list[Operation]]):
    def __init__(
        self,
        operation_service: OperationService,
        operation_db_gateway: OperationsReader,
        id_provider: IdProvider,
        uow: Commiter,
    ) -> None:
        self.operation_service = operation_service
        self.operation_db_gateway = operation_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: InputData) -> list[Operation]:
        user_id = await self.id_provider.get_current_user_id()

        return await self.operation_db_gateway.find_operations_by_user(
            user_id,
            data.from_time,
            data.to_time,
        )
