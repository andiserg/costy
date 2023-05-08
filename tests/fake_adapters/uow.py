from src.app.services.uow.abstract import AbstractUnitOfWork
from tests.fake_adapters.operations import FakeOperationRepository
from tests.fake_adapters.users import FakeUserRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    async def __aenter__(self):
        self.users = FakeUserRepository()
        self.operations = FakeOperationRepository()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return True

    async def _commit(self):
        pass

    async def rollback(self):
        pass
