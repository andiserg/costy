from dataclasses import dataclass
from typing import Protocol

from ..common.operation_gateway import OperationReader, OperationUpdater
from ...domain.exceptions.access import AccessDeniedError
from ...domain.exceptions.base import InvalidRequestError
from ...domain.models.category import CategoryId
from ...domain.models.operation import OperationId
from ...domain.sentinel import Sentinel
from ...domain.services.access import AccessService
from ...domain.services.operation import OperationService
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.commiter import Commiter


class OperationGateway(OperationReader, OperationUpdater, Protocol): ...


@dataclass(slots=True, kw_only=True)
class UpdateOperationData:
    amount: int | None = None
    description: str | None | type[Sentinel] = Sentinel
    time: int | None = None
    category_id: CategoryId | None | type[Sentinel] = Sentinel


@dataclass
class InputData:
    operation_id: OperationId
    data: UpdateOperationData


class UpdateOperation(Interactor[InputData, None]):
    def __init__(
        self,
        operation_service: OperationService,
        access_service: AccessService,
        operation_db_gateway: OperationGateway,
        id_provider: IdProvider,
        uow: Commiter,
    ):
        self.operation_service = operation_service
        self.access_service = access_service
        self.operation_db_gateway = operation_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: InputData) -> None:
        user_id = await self.id_provider.get_current_user_id()
        operation = await self.operation_db_gateway.get_operation(data.operation_id)

        if not operation or not operation.id:
            raise InvalidRequestError("Operation does not exist")

        if not self.access_service.ensure_can_edit(operation, user_id):
            raise AccessDeniedError("User can't edit this operation.")

        self.operation_service.update(
            operation,
            data.data.amount,
            data.data.description,
            data.data.time,
            data.data.category_id,
        )
        await self.operation_db_gateway.update_operation(operation.id, operation)
        await self.uow.commit()
