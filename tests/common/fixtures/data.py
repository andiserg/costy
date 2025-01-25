from random import choice, randint

from pytest_asyncio import fixture

from costy.adapters.bankapi.bank_gateway import MCCBankOperation
from costy.domain.models.operation import Operation


@fixture(scope="session")
async def user_id() -> int:
    return 999


@fixture
async def auth_id() -> str:
    return "auth_id"


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
