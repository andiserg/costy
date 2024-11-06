from dataclasses import dataclass

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, put

from costy.application.operation import (
    create_operation,
    delete_operation,
    read_list_operation,
    update_operation,
)
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
        service: FromDishka[read_list_operation.ReadListOperation],
        from_time: int | None,
        to_time: int | None,
    ) -> list[Operation]:
        data = read_list_operation.InputData(from_time, to_time)
        return await service(data)

    @post()
    @inject
    async def create_operation(
        self,
        service: FromDishka[create_operation.CreateOperation],
        data: create_operation.InputData,
    ) -> OperationId:
        return await service(data)

    @delete("{operation_id:int}")
    @inject
    async def delete_operation(
        self,
        operation_id: int,
        service: FromDishka[delete_operation.DeleteOperation],
    ) -> None:
        await service(OperationId(operation_id))

    @put("{operation_id:int}")
    @inject
    async def update_operation(
        self,
        operation_id: int,
        service: FromDishka[update_operation.UpdateOperation],
        pure_data: UpdateOperationPureData,
    ) -> None:
        description = pure_data.description if pure_data.description != "" else Sentinel
        data = update_operation.UpdateOperationData(
            amount=pure_data.amount,
            description=description,
            time=pure_data.time,
            category_id=pure_data.category_id or Sentinel,
        )
        request_data = update_operation.InputData(OperationId(operation_id), data)
        await service(request_data)
