from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.bank_api.bank_info import BankInfoRepository
from src.app.repositories.operations import OperationRepository
from src.app.repositories.users import UserRepository
from src.app.services.uow.abstract import AbstractUnitOfWork


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.users = UserRepository(self.session)
        self.operations = OperationRepository(self.session)
        self.banks_info = BankInfoRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
