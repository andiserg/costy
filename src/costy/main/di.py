from datetime import timedelta
from typing import Any, AsyncIterable

from dishka import AnyOf, Provider, Scope, from_context, provide
from httpx import AsyncClient
from litestar import Request
from litestar.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from costy.adapters.auth.auth_gateway import AuthGateway
from costy.adapters.auth.token import JwtTokenProcessor, KeySetProvider, TokenIdProvider
from costy.adapters.bankapi.bank_gateway import BankAdapter
from costy.adapters.bankapi.bankapi import BankAPIAdapter
from costy.adapters.bankapi.monobank import MonobankAdapter
from costy.adapters.db.category_gateway import CategoryAdapter
from costy.adapters.db.operation_gateway import OperationAdapter
from costy.adapters.db.user_gateway import UserAdapter
from costy.application.authenticate import Authenticate
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
from costy.application.common.auth_gateway import AuthLoger, AuthRegister
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
from costy.application.common.user_gateway import UserReader, UserSaver
from costy.application.operation import delete_operation, update_operation
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

AG = AuthGateway
UG = UserAdapter
OG = OperationAdapter
CG = CategoryAdapter
BG = BankAPIAdapter

IDP = IdProvider
AS = AsyncSession


class IdDIProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_id_provider(
        self,
        r: Request,  # type: ignore[type-arg]
        web_session: AsyncClient,
        settings: AuthSettings,
        user_gateway: UserAdapter,
    ) -> IDP:
        token_processor = JwtTokenProcessor("RS256", settings.audience, settings.issuer)
        jwsk_provider = KeySetProvider(
            settings.jwks_uri,
            web_session,
            timedelta(days=1),
        )

        id_provider = TokenIdProvider(token_processor, jwsk_provider)

        authorization = r.headers.get("authorization")
        if not authorization:
            raise HTTPException("Not authenticated", status_code=401)

        token_type, token = authorization.split(" ")
        id_provider.token = token
        id_provider.user_gateway = user_gateway
        return id_provider


class DIProvider(Provider):
    scope = Scope.REQUEST

    web_session = from_context(provides=AsyncClient, scope=Scope.APP)
    session_maker = from_context(
        provides=async_sessionmaker[AsyncSession], scope=Scope.APP,
    )
    auth_settings = from_context(provides=AuthSettings, scope=Scope.APP)
    banks_conf = from_context(provides=dict[str, dict[str, Any]], scope=Scope.APP)

    r = from_context(provides=Request, scope=Scope.REQUEST)

    user_service = provide(UserService)
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

    auth_gateway = provide(
        scope=Scope.REQUEST,
        source=AuthGateway,
        provides=AnyOf[AuthLoger, AuthRegister],
    )
    user_gateway = provide(
        scope=Scope.REQUEST,
        source=UserAdapter,
        provides=AnyOf[UserSaver, UserReader],
    )
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

    get_authenticate = provide(Authenticate, scope=Scope.REQUEST)
    get_create_user = provide(CreateUser)
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
