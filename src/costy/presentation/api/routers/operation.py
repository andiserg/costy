from dataclasses import dataclass

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, put

from costy.application.common.operation.dto import (
    ListOperationDTO,
    NewOperationDTO,
    UpdateOperationData,
    UpdateOperationDTO,
)
from costy.application.operation.create_operation import CreateOperation
from costy.application.operation.delete_operation import DeleteOperation
from costy.application.operation.read_list_operation import ReadListOperation
from costy.application.operation.update_operation import UpdateOperation
from costy.domain.models.category import CategoryId
from costy.domain.models.operation import Operation, OperationId
from costy.domain.sentinel import Sentinel


@dataclass(slots=True, kw_only=True)
class UpdateOperationPureData:
    """Dataclass without user defined types for OpenAPI"""
    amount: int | None = None
    description: str | None = ""  # Sentinel value
    time: int | None = None
    category_id: CategoryId | None = None


class OperationController(Controller):
    path = "/operations"
    tags = ("Operations",)

    @get()
    @inject
    async def get_list_operations(
        self,
        read_operations: FromDishka[ReadListOperation],
        from_time: int | None,
        to_time: int | None,
    ) -> list[Operation]:
        data = ListOperationDTO(from_time, to_time)
        return await read_operations(data)

    @post()
    @inject
    async def create_operation(
        self,
        create_operation: FromDishka[CreateOperation],
        data: NewOperationDTO,
    ) -> OperationId:
        return await create_operation(data)

    @delete("{operation_id:int}")
    @inject
    async def delete_operation(
        self,
        operation_id: int,
        delete_operation: FromDishka[DeleteOperation]
    ) -> None:
        await delete_operation(OperationId(operation_id))

    @put("{operation_id:int}")
    @inject
    async def update_operation(
        self,
        operation_id: int,
        update_operation: FromDishka[UpdateOperation],
        pure_data: UpdateOperationPureData,
    ) -> None:
        data = UpdateOperationData(
            amount=pure_data.amount,
            description=pure_data.description if pure_data.description != "" else Sentinel,
            time=pure_data.time,
            category_id=pure_data.category_id or Sentinel,
        )
        request_data = UpdateOperationDTO(OperationId(operation_id), data)
        await update_operation(request_data)
