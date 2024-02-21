from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from adaptix import Retort
from aiohttp import ClientSession
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from costy.adapters.auth.auth_gateway import AuthGateway
from costy.adapters.db.category_gateway import CategoryGateway
from costy.adapters.db.operation_gateway import OperationGateway
from costy.adapters.db.uow import OrmUoW
from costy.adapters.db.user_gateway import UserGateway
from costy.application.authenticate import Authenticate
from costy.application.category.create_category import CreateCategory
from costy.application.category.read_available_categories import (
    ReadAvailableCategories,
)
from costy.application.common.id_provider import IdProvider
from costy.application.operation.create_operation import CreateOperation
from costy.application.operation.read_list_operation import ReadListOperation
from costy.application.operation.read_operation import ReadOperation
from costy.application.user.create_user import CreateUser
from costy.domain.services.category import CategoryService
from costy.domain.services.operation import OperationService
from costy.domain.services.user import UserService
from costy.infrastructure.config import AuthSettings
from costy.presentation.interactor_factory import InteractorFactory


@dataclass
class Depends:
    session: AsyncSession
    web_session: ClientSession
    uow: OrmUoW
    auth_gateway: AuthGateway


class IoC(InteractorFactory):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        web_session: ClientSession,
        tables: dict[str, Table],
        retort: Retort,
        auth_settings: AuthSettings
    ):
        self._session_factory = session_factory
        self._web_session = web_session
        self._tables = tables
        self._retort = retort
        self._settings = auth_settings

    @asynccontextmanager
    async def _init_depends(self) -> AsyncIterator[Depends]:
        session = self._session_factory()
        auth_gateway = AuthGateway(session, self._web_session, self._tables["users"], self._settings)
        yield Depends(session, self._web_session, OrmUoW(session), auth_gateway)
        await session.close()

    @asynccontextmanager
    async def authenticate(self) -> AsyncIterator[Authenticate]:
        async with self._init_depends() as depends:
            yield Authenticate(
                depends.auth_gateway,
                depends.uow
            )

    @asynccontextmanager
    async def create_user(self) -> AsyncIterator[CreateUser]:
        async with self._init_depends() as depends:
            yield CreateUser(
                UserService(), UserGateway(depends.session, self._tables["users"], self._retort), depends.uow
            )

    @asynccontextmanager
    async def create_operation(
            self, id_provider: IdProvider
    ) -> AsyncIterator[CreateOperation]:
        async with self._init_depends() as depends:
            id_provider.auth_gateway = depends.auth_gateway  # type: ignore
            yield CreateOperation(
                OperationService(),
                OperationGateway(depends.session, self._tables["operations"], self._retort),
                id_provider, depends.uow
            )

    @asynccontextmanager
    async def read_operation(
            self, id_provider: IdProvider
    ) -> AsyncIterator[ReadOperation]:
        async with self._init_depends() as depends:
            id_provider.auth_gateway = depends.auth_gateway  # type: ignore
            yield ReadOperation(
                OperationService(),
                OperationGateway(depends.session, self._tables["operations"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def read_list_operation(
            self, id_provider: IdProvider
    ) -> AsyncIterator[ReadListOperation]:
        async with self._init_depends() as depends:
            id_provider.auth_gateway = depends.auth_gateway  # type: ignore
            yield ReadListOperation(
                OperationService(),
                OperationGateway(depends.session, self._tables["operations"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def create_category(
            self, id_provider: IdProvider
    ) -> AsyncIterator[CreateCategory]:
        async with self._init_depends() as depends:
            id_provider.auth_gateway = depends.auth_gateway  # type: ignore
            yield CreateCategory(
                CategoryService(),
                CategoryGateway(depends.session, self._tables["categories"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def read_available_categories(
            self, id_provider: IdProvider
    ) -> AsyncIterator[ReadAvailableCategories]:
        async with self._init_depends() as depends:
            id_provider.auth_gateway = depends.auth_gateway  # type: ignore
            yield ReadAvailableCategories(
                CategoryService(),
                CategoryGateway(depends.session, self._tables["categories"], self._retort),
                id_provider,
                depends.uow
            )
