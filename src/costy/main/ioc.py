from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from costy.adapters.db.category_gateway import CategoryGateway
from costy.adapters.db.operation_gateway import OperationGateway
from costy.adapters.db.uow import OrmUoW
from costy.adapters.db.user_gateway import UserGateway
from costy.application.authenticate import Authenticate
from costy.application.category.create_category import CreateCategory
from costy.application.category.read_available_categories import ReadAvailableCategories
from costy.application.common.id_provider import IdProvider
from costy.application.operation.create_operation import CreateOperation
from costy.application.operation.read_list_operation import ReadListOperation
from costy.application.operation.read_operation import ReadOperation
from costy.application.user.create_user import CreateUser
from costy.domain.services.category import CategoryService
from costy.domain.services.operation import OperationService
from costy.domain.services.user import UserService
from costy.presentation.interactor_factory import InteractorFactory


@dataclass
class Depends:
    session: AsyncSession
    uow: OrmUoW


class IoC(InteractorFactory):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    @asynccontextmanager
    async def _init_depends(self) -> AsyncContextManager[Depends]:
        async with self._session_factory() as session:
            yield Depends(session, OrmUoW(session))

    @asynccontextmanager
    async def authenticate(self) -> AsyncContextManager[Authenticate]:
        async with self._init_depends() as depends:
            yield Authenticate(UserGateway(depends.session), depends.uow)

    @asynccontextmanager
    async def create_user(self) -> AsyncContextManager[CreateUser]:
        async with self._init_depends() as depends:
            yield CreateUser(UserService(), UserGateway(depends.session), depends.uow)

    @asynccontextmanager
    async def create_operation(self, id_provider: IdProvider) -> AsyncContextManager[CreateOperation]:
        async with self._init_depends() as depends:
            yield CreateOperation(OperationService(), OperationGateway(depends.session), id_provider, depends.uow)

    @asynccontextmanager
    async def read_operation(self, id_provider: IdProvider) -> AsyncContextManager[ReadOperation]:
        async with self._init_depends() as depends:
            yield ReadOperation(OperationService(), OperationGateway(depends.session), id_provider, depends.uow)

    @asynccontextmanager
    async def read_list_operation(self, id_provider: IdProvider) -> AsyncContextManager[ReadListOperation]:
        async with self._init_depends() as depends:
            yield ReadListOperation(OperationService(), OperationGateway(depends.session), id_provider, depends.uow)

    @asynccontextmanager
    async def create_category(self, id_provider: IdProvider) -> AsyncContextManager[CreateCategory]:
        async with self._init_depends() as depends:
            yield CreateCategory(CategoryService(), CategoryGateway(depends.session), id_provider, depends.uow)

    @asynccontextmanager
    async def read_available_categories(self, id_provider: IdProvider) -> AsyncContextManager[ReadAvailableCategories]:
        async with self._init_depends() as depends:
            yield ReadAvailableCategories(CategoryService(), CategoryGateway(depends.session), id_provider, depends.uow)
