from src.app.services.uow.abstract import AbstractUnitOfWork
from tests.fake_adapters.bank_info import FakeBankInfoRepository
from tests.fake_adapters.categories import FakeCategoryRepository
from tests.fake_adapters.operations import FakeOperationRepository
from tests.fake_adapters.users import FakeUserRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = FakeUserRepository()
        self.operations = FakeOperationRepository()
        self.categories = FakeCategoryRepository()
        self.banks_info = FakeBankInfoRepository()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _commit(self):
        pass

    async def rollback(self):
        pass
