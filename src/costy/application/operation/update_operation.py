from typing import Protocol

from ...domain.exceptions.access import AccessDeniedError
from ...domain.exceptions.base import InvalidRequestError
from ...domain.services.access import AccessService
from ...domain.services.operation import OperationService
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.operation_gateway import OperationReader, OperationUpdater
from ..common.uow import UoW
from ..operation.dto import UpdateOperationDTO


class OperationGateway(OperationReader, OperationUpdater, Protocol):
    ...


class UpdateOperation(Interactor[UpdateOperationDTO, None]):
    def __init__(
        self,
        operation_service: OperationService,
        access_service: AccessService,
        operation_db_gateway: OperationGateway,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.operation_service = operation_service
        self.access_service = access_service
        self.operation_db_gateway = operation_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: UpdateOperationDTO) -> None:
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
            data.data.category_id
        )
        await self.operation_db_gateway.update_operation(operation.id, operation)
        await self.uow.commit()
