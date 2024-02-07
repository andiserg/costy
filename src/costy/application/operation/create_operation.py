from dataclasses import dataclass

from costy.application.common.id_provider import IdProvider
from costy.application.common.interactor import Interactor
from costy.application.common.operation_gateway import OperationSaver
from costy.application.common.uow import UoW
from costy.domain.models.category import CategoryId
from costy.domain.models.operation import OperationId
from costy.domain.services.operation import OperationService


@dataclass
class NewOperationDTO:
    amount: int
    description: str | None
    time: int
    category_id: CategoryId


class CreateOperation(Interactor[NewOperationDTO, OperationId]):
    def __init__(
        self,
        operation_service: OperationService,
        operation_db_gateway: OperationSaver,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.operation_service = operation_service
        self.operation_db_gateway = operation_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: NewOperationDTO) -> OperationId:
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
        return operation_id  # type: ignore
