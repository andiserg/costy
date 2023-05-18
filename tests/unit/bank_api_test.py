import json

import pytest

from src.app.domain.categories import Category
from src.app.services.bank_api import get_costs_by_bank, update_banks_costs
from tests.fake_adapters.bank_api import FakeBankManagerRepository
from tests.fake_adapters.uow import FakeUnitOfWork


def set_mcc_categories_to_repo(uow: FakeUnitOfWork):
    with open("../../src/app/repositories/mcc.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        uow.categories.instances = [
            Category(name=key, type="mcc", user_id=None) for key in data.keys()
        ]


@pytest.mark.asyncio
async def test_get_costs():
    repo = FakeBankManagerRepository(properties={"id": 1, "user_id": 1})
    costs = await get_costs_by_bank(repo)
    assert len(costs) == 9


@pytest.mark.asyncio
async def test_update_costs():
    uow = FakeUnitOfWork()
    set_mcc_categories_to_repo(uow)
    repo = FakeBankManagerRepository(properties={"id": 1, "user_id": 1})
    await update_banks_costs(uow, [repo])
    assert len(uow.operations.instances) == 9
