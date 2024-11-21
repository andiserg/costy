from dataclasses import dataclass
from datetime import UTC, datetime

from ...domain.models.category import CategoryId
from ...domain.models.operation import OperationId
from ...domain.services.operation import OperationService
from ..common.commiter import Commiter
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.operation_gateway import OperationSaver


@dataclass(slots=True, kw_only=True)
class InputData:
    amount: int
    description: str | None = None
    time: int = int(datetime.now(tz=UTC).timestamp())
    category_id: CategoryId


class CreateOperation(Interactor[InputData, OperationId]):
    def __init__(
        self,
        operation_service: OperationService,
        operation_db_gateway: OperationSaver,
        id_provider: IdProvider,
        uow: Commiter,
    ) -> None:
        self.operation_service = operation_service
        self.operation_db_gateway = operation_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: InputData) -> OperationId:
        user_id = await self.id_provider.get_current_user_id()
        operation = self.operation_service.create(
            data.amount,
            data.description,
            data.time,
            user_id,
            data.category_id,
        )
        await self.operation_db_gateway.save_operation(operation)
        operation_id = operation.id
        await self.uow.commit()
        return operation_id  # type: ignore[return-value]
