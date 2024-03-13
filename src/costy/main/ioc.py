from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator

from adaptix import Retort
from httpx import AsyncClient
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from costy.adapters.auth.auth_gateway import AuthGateway
from costy.adapters.bankapi.bank_gateway import BankGateway
from costy.adapters.bankapi.bankapi import BankAPIGateway
from costy.adapters.bankapi.monobank import MonobankGateway
from costy.adapters.db.category_gateway import CategoryGateway
from costy.adapters.db.operation_gateway import OperationGateway
from costy.adapters.db.user_gateway import UserGateway
from costy.application.authenticate import Authenticate
from costy.application.bankapi.create_bankapi import CreateBankAPI
from costy.application.bankapi.delete_bankapi import DeleteBankAPI
from costy.application.bankapi.read_bankapi_list import ReadBankapiList
from costy.application.bankapi.update_bank_operations import (
    UpdateBankOperations,
)
from costy.application.category.create_category import CreateCategory
from costy.application.category.delete_category import DeleteCategory
from costy.application.category.read_available_categories import (
    ReadAvailableCategories,
)
from costy.application.category.update_category import UpdateCategory
from costy.application.common.id_provider import IdProvider
from costy.application.operation.create_operation import CreateOperation
from costy.application.operation.delete_operation import DeleteOperation
from costy.application.operation.read_list_operation import ReadListOperation
from costy.application.operation.update_operation import UpdateOperation
from costy.application.user.create_user import CreateUser
from costy.domain.services.access import AccessService
from costy.domain.services.bankapi import BankAPIService
from costy.domain.services.category import CategoryService
from costy.domain.services.operation import OperationService
from costy.domain.services.user import UserService
from costy.infrastructure.config import AuthSettings
from costy.presentation.interactor_factory import InteractorFactory


@dataclass
class Depends:
    session: AsyncSession
    web_session: AsyncClient
    uow: AsyncSession
    user_gateway: UserGateway


class IoC(InteractorFactory):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        web_session: AsyncClient,
        tables: dict[str, Table],
        retort: Retort,
        auth_settings: AuthSettings,
        banks_conf: dict[str, Any]
    ):
        self._session_factory = session_factory
        self._web_session = web_session
        self._tables = tables
        self._retort = retort
        self._settings = auth_settings
        self._banks_conf = banks_conf
        self._bank_gateways = self._init_bank_gateways()

    def _init_bank_gateways(self) -> dict[str, BankGateway]:
        return {
            "monobank": MonobankGateway(self._web_session, self._banks_conf, self._retort)
        }

    @asynccontextmanager
    async def _init_depends(self) -> AsyncIterator[Depends]:
        session = self._session_factory()
        user_gateway = UserGateway(session, self._tables["users"], self._retort)
        yield Depends(session, self._web_session, session, user_gateway)
        await session.close()

    @asynccontextmanager
    async def authenticate(self) -> AsyncIterator[Authenticate]:
        async with self._init_depends() as depends:
            yield Authenticate(
                AuthGateway(depends.session, self._web_session, self._tables["users"], self._settings),
                depends.uow
            )

    @asynccontextmanager
    async def create_user(self) -> AsyncIterator[CreateUser]:
        async with self._init_depends() as depends:
            yield CreateUser(
                UserService(),
                depends.user_gateway,
                AuthGateway(depends.session, self._web_session, self._tables["users"], self._settings),
                depends.uow
            )

    @asynccontextmanager
    async def create_operation(
            self, id_provider: IdProvider
    ) -> AsyncIterator[CreateOperation]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield CreateOperation(
                OperationService(),
                OperationGateway(depends.session, self._tables["operations"], self._retort),
                id_provider, depends.uow
            )

    @asynccontextmanager
    async def read_list_operation(
            self, id_provider: IdProvider
    ) -> AsyncIterator[ReadListOperation]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield ReadListOperation(
                OperationService(),
                OperationGateway(depends.session, self._tables["operations"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def delete_operation(
            self, id_provider: IdProvider
    ) -> AsyncIterator[DeleteOperation]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield DeleteOperation(
                AccessService(),
                OperationGateway(depends.session, self._tables["operations"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def update_operation(
            self, id_provider: IdProvider
    ) -> AsyncIterator[UpdateOperation]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield UpdateOperation(
                OperationService(),
                AccessService(),
                OperationGateway(depends.session, self._tables["operations"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def create_category(
            self, id_provider: IdProvider
    ) -> AsyncIterator[CreateCategory]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield CreateCategory(
                CategoryService(),
                CategoryGateway(depends.session, self._tables["categories"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def delete_category(
            self, id_provider: IdProvider
    ) -> AsyncIterator[DeleteCategory]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield DeleteCategory(
                AccessService(),
                CategoryGateway(depends.session, self._tables["categories"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def update_category(
            self, id_provider: IdProvider
    ) -> AsyncIterator[UpdateCategory]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield UpdateCategory(
                CategoryService(),
                AccessService(),
                CategoryGateway(depends.session, self._tables["categories"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def read_available_categories(
            self, id_provider: IdProvider
    ) -> AsyncIterator[ReadAvailableCategories]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield ReadAvailableCategories(
                CategoryService(),
                CategoryGateway(depends.session, self._tables["categories"], self._retort),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def create_bankapi(
        self, id_provider: IdProvider
    ) -> AsyncIterator[CreateBankAPI]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield CreateBankAPI(
                BankAPIService(),
                BankAPIGateway(
                    depends.session,
                    depends.web_session,
                    self._tables["bankapis"],
                    self._retort,
                    self._bank_gateways,
                    self._banks_conf
                ),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def delete_bankapi(
        self, id_provider: IdProvider
    ) -> AsyncIterator[DeleteBankAPI]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield DeleteBankAPI(
                AccessService(),
                BankAPIGateway(
                    depends.session,
                    depends.web_session,
                    self._tables["bankapis"],
                    self._retort,
                    self._bank_gateways,
                    self._banks_conf
                ),
                id_provider,
                depends.uow
            )

    @asynccontextmanager
    async def read_bankapi_list(
        self, id_provider: IdProvider
    ) -> AsyncIterator[ReadBankapiList]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield ReadBankapiList(
                BankAPIGateway(
                    depends.session,
                    depends.web_session,
                    self._tables["bankapis"],
                    self._retort,
                    self._bank_gateways,
                    self._banks_conf
                ),
                id_provider,
            )

    @asynccontextmanager
    async def update_bank_operations(
        self, id_provider: IdProvider
    ) -> AsyncIterator[UpdateBankOperations]:
        async with self._init_depends() as depends:
            id_provider.user_gateway = depends.user_gateway  # type: ignore
            yield UpdateBankOperations(
                BankAPIService(),
                OperationService(),
                BankAPIGateway(
                    depends.session,
                    depends.web_session,
                    self._tables["bankapis"],
                    self._retort,
                    self._bank_gateways,
                    self._banks_conf
                ),
                OperationGateway(depends.session, self._tables["operations"], self._retort),
                CategoryGateway(depends.session, self._tables["categories"], self._retort),
                id_provider,
                depends.uow,
            )
