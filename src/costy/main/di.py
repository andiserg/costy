from typing import Any, AsyncIterable

from dishka import AnyOf, Provider, Scope, from_context, provide
from httpx import AsyncClient
from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from costy.adapters.auth.token import TokenIdProvider
from costy.adapters.bankapi.bank_gateway import BankAdapter
from costy.adapters.bankapi.bankapi import BankAPIAdapter
from costy.adapters.bankapi.banks.monobank import MonobankAdapter
from costy.adapters.db.category_gateway import CategoryAdapter
from costy.adapters.db.operation_gateway import OperationAdapter
from costy.application.bankapi import (
    create_bankapi,
    delete_bankapi,
    update_bank_operations,
)
from costy.application.bankapi.create_bankapi import CreateBankAPI
from costy.application.bankapi.delete_bankapi import DeleteBankAPI
from costy.application.bankapi.read_bankapi_list import ReadBankapiList
from costy.application.bankapi.update_bank_operations import UpdateBankOperations
from costy.application.category import delete_category, update_category
from costy.application.category.create_category import CreateCategory
from costy.application.category.delete_category import DeleteCategory
from costy.application.category.read_available_categories import ReadAvailableCategories
from costy.application.category.update_category import UpdateCategory
from costy.application.common.bankapi_gateway import (
    BankAPIBanksReader,
    BankAPIBulkUpdater,
    BankAPIDeleter,
    BankAPIOperationsReader,
    BankAPIReader,
    BankAPISaver,
    BanksAPIReader,
)
from costy.application.common.category_gateway import (
    CategoriesFinder,
    CategoriesReader,
    CategoryDeleter,
    CategoryFinder,
    CategoryReader,
    CategorySaver,
    CategoryUpdater,
)
from costy.application.common.commiter import Commiter
from costy.application.common.id_provider import IdProvider
from costy.application.common.operation_gateway import (
    OperationDeleter,
    OperationReader,
    OperationSaver,
    OperationsBulkSaver,
    OperationsReader,
)
from costy.application.operation import delete_operation, update_operation
from costy.application.operation.create_operation import CreateOperation
from costy.application.operation.delete_operation import DeleteOperation
from costy.application.operation.read_list_operation import ReadListOperation
from costy.application.operation.update_operation import UpdateOperation
from costy.domain.services.access import AccessService
from costy.domain.services.bankapi import BankAPIService
from costy.domain.services.category import CategoryService
from costy.domain.services.operation import OperationService


class IdDIProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_id_provider(
        self,
        r: Request,  # type: ignore[type-arg]
    ) -> IdProvider:
        return TokenIdProvider(r.headers.get("user_id", ""))


class DIProvider(Provider):
    scope = Scope.REQUEST

    web_session = from_context(provides=AsyncClient, scope=Scope.APP)
    session_maker = from_context(
        provides=async_sessionmaker[AsyncSession], scope=Scope.APP,
    )
    banks_conf = from_context(provides=dict[str, dict[str, Any]], scope=Scope.APP)

    r = from_context(provides=Request, scope=Scope.REQUEST)

    bank_service = provide(BankAPIService)
    operation_service = provide(OperationService)
    category_service = provide(CategoryService)
    access_service = provide(AccessService)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, Commiter]]:
        async with session_maker() as session:
            yield session

    operation_gateway = provide(
        scope=Scope.REQUEST,
        source=OperationAdapter,
        provides=AnyOf[
            OperationReader,
            OperationSaver,
            OperationDeleter,
            OperationsReader,
            OperationsBulkSaver,
            OperationAdapter,

            update_operation.OperationGateway,
            delete_operation.OperationGateway,
        ],
    )
    category_gateway = provide(
        scope=Scope.REQUEST,
        source=CategoryAdapter,
        provides=AnyOf[
            CategoryReader,
            CategoryFinder,
            CategorySaver,
            CategoryDeleter,
            CategoriesReader,
            CategoryUpdater,
            CategoriesFinder,
            CategoryAdapter,

            update_category.CategoryGateway,
            delete_category.CategoryGateway,
            update_bank_operations.CategoryGateway,
        ],
    )
    bankapi_gateway = provide(
        scope=Scope.REQUEST,
        source=BankAPIAdapter,
        provides=AnyOf[
            BankAPISaver,
            BankAPIDeleter,
            BankAPIBanksReader,
            BankAPIReader,
            BanksAPIReader,
            BankAPIBulkUpdater,
            BankAPIOperationsReader,
            BankAPIAdapter,

            create_bankapi.BankAPIGateway,
            delete_bankapi.BankAPIGateway,
            update_bank_operations.BankAPIGateway,
        ],
    )

    @provide(scope=Scope.REQUEST)
    async def get_bank_gateways(
        self,
        web_session: AsyncClient,
        banks_conf: dict[str, dict[str, Any]],
    ) -> dict[str, BankAdapter]:
        return {
            "monobank": MonobankAdapter(web_session, banks_conf),
        }

    get_create_operation = provide(CreateOperation)
    get_read_list_operation = provide(ReadListOperation)
    get_delete_operation = provide(DeleteOperation)
    get_update_operation = provide(UpdateOperation)
    get_create_category = provide(CreateCategory)
    get_delete_category = provide(DeleteCategory)
    get_update_category = provide(UpdateCategory)
    get_read_available_categories = provide(ReadAvailableCategories)
    get_create_bankapi = provide(CreateBankAPI)
    get_delete_bankapi = provide(DeleteBankAPI)
    get_read_bankapi_list = provide(ReadBankapiList)
    get_update_bank_operations = provide(UpdateBankOperations)
