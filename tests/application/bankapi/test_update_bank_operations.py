from random import choice, randint
from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.bankapi.update_bank_operations import (
    UpdateBankOperations,
)
from costy.application.common.bankapi.dto import BankOperationDTO
from costy.application.common.category.category_gateway import CategoryFinder
from costy.application.common.uow import UoW
from costy.domain.models.bankapi import BankAPI, BankApiId
from costy.domain.models.category import Category, CategoryId
from costy.domain.models.operation import Operation
from costy.domain.services.bankapi import BankAPIService
from costy.domain.services.operation import OperationService


@fixture
async def existing_mcc() -> list[int]:
    return [1, 2, 3]


@fixture
async def interactor(id_provider, user_id, existing_mcc) -> UpdateBankOperations:
    bankapi_gateway = Mock()
    bankapi_gateway.operations = []
    operation_gateway = Mock()
    category_gateway = Mock(spec=CategoryFinder)
    category_gateway.find_category.return_value = Category(id=CategoryId(9999), name="Other")
    mcc_list = existing_mcc + [4, 5]

    async def get_bankapi_list(*args, **kwargs):
        return [
            BankAPI(
                id=0,
                user_id=user_id,
                name="bank1",
                access_data={"key1": "value1"},
            ),
            BankAPI(
                id=1,
                user_id=user_id,
                name="bank2",
                access_data={"key2": "value2"},
            )]

    async def read_bank_operations(bankapi: BankAPI, **kwargs):
        result = [
            BankOperationDTO(
                operation=Operation(
                    id=BankApiId(bankapi.id * 10 + i),  # type: ignore
                    user_id=user_id,
                    bank_name=bankapi.name,
                    category_id=None,
                    amount=randint(1, 100),
                    time=1111,
                ),
                mcc=choice(mcc_list)
            )
            for i in range(randint(5, 10))
        ]
        bankapi_gateway.operations.extend(result)
        return result

    async def update_bankapis(*args):
        pass

    bankapi_gateway.get_bankapi_list = get_bankapi_list
    bankapi_gateway.update_bankapis = update_bankapis
    bankapi_gateway.read_bank_operations = read_bank_operations

    async def save_operarions(operations: list[Operation]):
        operation_gateway.operations = operations

    operation_gateway.save_operations = save_operarions

    async def find_categories(mcc_codes):
        return {
            mcc: Category(
                id=mcc * 10,
                name="test",
            ) for mcc in mcc_codes if mcc in existing_mcc
        }

    category_gateway.find_categories_by_mcc_codes = find_categories

    return UpdateBankOperations(
        BankAPIService(),
        OperationService(),
        bankapi_gateway,
        operation_gateway,
        category_gateway,
        id_provider,
        Mock(spec=UoW)
    )


@pytest.mark.asyncio
async def test_update_bank_operations(interactor, existing_mcc):
    await interactor()

    bank_operations = interactor._bankapi_gateway.operations
    result = interactor._operation_gateway.operations

    assert all(
        (
            bank_operation.mcc in existing_mcc and operation.category_id
        ) or (
            bank_operation.mcc not in existing_mcc and operation.category_id == 9999
        ) for bank_operation, operation in zip(bank_operations, result)
    )
