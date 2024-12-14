import os
from random import choice, randint

import pytest
from pytest_asyncio import fixture

from costy.adapters.bankapi.bank_gateway import MCCBankOperation
from costy.application.authenticate import InputData
from costy.application.category import create_category
from costy.application.operation import create_operation
from costy.domain.models.bankapi import BankApiId
from costy.domain.models.category import Category, CategoryId
from costy.domain.models.operation import Operation, OperationId


@fixture(scope="session")
async def user_id() -> int:
    return 999


@fixture
async def operation_id() -> OperationId:
    return OperationId(999)


@fixture
async def category_id() -> CategoryId:
    return CategoryId(999)


@fixture
async def bankapi_id() -> BankApiId:
    return BankApiId(888)


@fixture
async def category_info() -> create_category.InputData:
    return create_category.InputData(name="test", view=None)


@fixture
async def operation_info() -> create_operation.InputData:
    return create_operation.InputData(
        amount=100,
        description="description",
        time=10000,
        category_id=CategoryId(999),
    )


# @fixture
# async def user_info() -> create_user.InputData:
#     return create_user.InputData(email="test@email.com", password="password")


@fixture
async def login_info() -> InputData:
    return InputData(email="test@email.com", password="password")


@fixture
async def token() -> str:
    return "token"


@fixture
async def auth_id() -> str:
    return "auth_id"


@fixture(scope="session")
async def auth_sub() -> str:  # type: ignore
    try:
        return os.environ["TEST_AUTH_USER_SUB"].replace("auth0|", "")
    except KeyError:
        pytest.fail("No test user sub environment variable.")


@fixture
async def credentials() -> dict[str, str]:  # type: ignore
    try:
        return {
            "username": os.environ["TEST_AUTH_USER"],
            "password": os.environ["TEST_AUTH_PASSWORD"],
        }
    except KeyError:
        pytest.fail("No test user credentials.")


@fixture
async def operation_list(user_id, category_id):
    return [
        Operation(
            id=0,
            user_id=user_id,
            amount=100,
            description="test description",
            category_id=category_id,
            time=1111,
        ),
        Operation(
            id=1,
            user_id=user_id,
            amount=100,
            description="test description",
            category_id=category_id,
            time=1111,
        ),
        Operation(
            id=2,
            user_id=user_id,
            amount=100,
            description="test description",
            category_id=category_id,
            time=1111,
        ),
        Operation(
            id=3,
            user_id=user_id,
            amount=100,
            description="test description",
            category_id=category_id,
            time=1111,
        ),
    ]


@fixture
async def category_list(user_id):
    return [
        Category(id=0, name="test", user_id=user_id),
        Category(id=1, name="test", user_id=user_id),
        Category(id=2, name="test", user_id=user_id),
    ]


@fixture(scope="session")
async def bank_operations(user_id):
    mcc_list = [1, 2, 3]

    return [
        MCCBankOperation(
            operation=Operation(
                id=None,
                amount=100,
                description="desc",
                time=1111,
                user_id=user_id,
                category_id=None,
            ),
            mcc=choice(mcc_list),
        )
        for _ in range(randint(5, 10))
    ]
