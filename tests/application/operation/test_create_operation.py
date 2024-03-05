from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.common.id_provider import IdProvider
from costy.application.common.operation_gateway import OperationSaver
from costy.application.common.uow import UoW
from costy.application.operation.create_operation import CreateOperation
from costy.application.operation.dto import NewOperationDTO
from costy.domain.models.operation import Operation, OperationId
from costy.domain.models.user import UserId


@fixture
async def interactor(id_provider: IdProvider, category_id: OperationId, user_id: UserId, operation_info: NewOperationDTO) -> CreateOperation:
    operation_service = Mock()
    operation_service.create.return_value = Operation(
        id=None,
        amount=operation_info.amount,
        description=operation_info.description,
        time=operation_info.time,
        user_id=user_id,
        category_id=operation_info.category_id,
    )

    async def save_operation_mock(operation: Operation) -> None:
        operation.id = category_id

    operation_gateway = Mock(spec=OperationSaver)
    operation_gateway.save_operation = save_operation_mock
    uow = Mock(spec=UoW)
    return CreateOperation(operation_service, operation_gateway, id_provider, uow)


@pytest.mark.asyncio
async def test_create_operation(interactor: CreateOperation, operation_info: NewOperationDTO, category_id: OperationId) -> None:
    assert await interactor(operation_info) == category_id
