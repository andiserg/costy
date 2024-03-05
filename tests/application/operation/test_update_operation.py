from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.common.uow import UoW
from costy.application.operation.dto import (
    UpdateOperationData,
    UpdateOperationDTO,
)
from costy.application.operation.update_operation import (
    OperationGateway,
    UpdateOperation,
)
from costy.domain.exceptions.access import AccessDeniedError
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.category import CategoryId
from costy.domain.models.operation import Operation, OperationId
from costy.domain.models.user import UserId
from costy.domain.services.access import AccessService
from costy.domain.services.operation import OperationService


@fixture
async def interactor(
        operation_id: OperationId,
        user_id: UserId,
        category_id: CategoryId,
        id_provider
) -> UpdateOperation:
    operation_gateway = Mock(spec=OperationGateway)
    operation_gateway.get_operation.return_value = Operation(
        operation_id,
        1000,
        "desc",
        1111,
        user_id,
        category_id
    )
    uow = Mock(spec=UoW)
    return UpdateOperation(OperationService(), AccessService(), operation_gateway, id_provider, uow)


@pytest.mark.asyncio
async def test_update_operation(interactor: UpdateOperation, operation_id: OperationId):
    update_data = UpdateOperationDTO(operation_id, UpdateOperationData(amount=2000))
    try:
        await interactor(update_data)
    except (AccessDeniedError, InvalidRequestError) as err:
        pytest.fail(f"Update operation interactor raise error: {err}")
