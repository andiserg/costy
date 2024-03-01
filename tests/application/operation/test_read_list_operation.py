from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.common.operation_gateway import OperationsReader
from costy.application.common.uow import UoW
from costy.application.operation.dto import ListOperationDTO
from costy.application.operation.read_list_operation import ReadListOperation


@fixture
async def interactor(id_provider, operation_list) -> ReadListOperation:
    operation_service = Mock()
    operation_gateway = Mock(spec=OperationsReader)
    operation_gateway.find_operations_by_user.return_value = operation_list
    uow = Mock(spec=UoW)
    return ReadListOperation(operation_service, operation_gateway, id_provider, uow)


@pytest.mark.asyncio
async def test_read_list_operation(interactor, operation_list):
    data = ListOperationDTO(from_time=None, to_time=None)
    assert await interactor(data) == operation_list
