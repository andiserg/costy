from litestar import Controller, delete, get, post, put

from costy.application.common.id_provider import IdProvider
from costy.application.operation.dto import (
    ListOperationDTO,
    NewOperationDTO,
    UpdateOperationData,
    UpdateOperationDTO,
)
from costy.domain.models.operation import Operation, OperationId
from costy.presentation.interactor_factory import InteractorFactory


class OperationController(Controller):
    path = '/operations'

    @get()
    async def get_list_operations(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        from_time: int | None,
        to_time: int | None,
    ) -> list[Operation]:
        data = ListOperationDTO(from_time, to_time)
        async with ioc.read_list_operation(id_provider) as read_operations:
            return await read_operations(data)

    @post()
    async def create_operation(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        data: NewOperationDTO,
    ) -> OperationId:
        async with ioc.create_operation(id_provider) as create_operation:
            return await create_operation(data)

    @delete("{operation_id:int}")
    async def delete_operation(
        self,
        operation_id: int,
        ioc: InteractorFactory,
        id_provider: IdProvider,
    ) -> None:
        async with ioc.delete_operation(id_provider) as delete_operation:
            await delete_operation(OperationId(operation_id))

    @put("{operation_id:int}")
    async def update_operation(
        self,
        operation_id: int,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        data: UpdateOperationData,
    ) -> None:
        async with ioc.update_operation(id_provider) as update_operation:
            request_data = UpdateOperationDTO(OperationId(operation_id), data)
            await update_operation(request_data)
