from typing import Protocol

from ...domain.exceptions.access import AccessDeniedError
from ...domain.exceptions.base import InvalidRequestError
from ...domain.models.operation import OperationId
from ...domain.services.access import AccessService
from ..common.commiter import Commiter
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.operation_gateway import OperationDeleter, OperationReader


class OperationGateway(OperationReader, OperationDeleter, Protocol): ...


class DeleteOperation(Interactor[OperationId, None]):
    def __init__(
        self,
        access_service: AccessService,
        operation_gateway: OperationGateway,
        id_provider: IdProvider,
        uow: Commiter,
    ) -> None:
        self.access_service = access_service
        self.operation_gateway = operation_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, operation_id: OperationId) -> None:
        user_id = await self.id_provider.get_current_user_id()
        operation = await self.operation_gateway.get_operation(operation_id)

        if not operation:
            raise InvalidRequestError("Operation does not exist")

        if not self.access_service.ensure_can_edit(operation, user_id):
            raise AccessDeniedError(
                "User does not have permission to delete this operation",
            )

        await self.operation_gateway.delete_operation(operation_id)
        await self.uow.commit()
