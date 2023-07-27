from src.app.domain.bank_api import BankInfo
from src.app.repositories.absctract.bank_api import ABankInfoRepository
from tests.fake_adapters.base import FakeRepository


class FakeBankInfoRepository(FakeRepository, ABankInfoRepository):
    async def get(self, **kwargs):
        pass

    async def get_all_by_user(self, user_id) -> list[BankInfo]:
        pass

    async def get_properties(self, manager: BankInfo) -> dict[str, str | int | float]:
        pass

    async def add_property(
        self, manager: BankInfo, name: str, value: str | int | float
    ):
        pass

    async def set_update_time_to_managers(self, ids: list[int]):
        pass

    async def delete(self, user_id: int, bank_name: str):
        pass
