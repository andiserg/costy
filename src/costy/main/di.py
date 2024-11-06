from datetime import timedelta
from typing import Any, AsyncIterable

from dishka import Provider, provide, Scope, from_context
from httpx import AsyncClient
from litestar import Request
from litestar.exceptions import HTTPException
from sqlalchemy import Table
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
from costy.application.bankapi.create_bankapi import CreateBankAPI
from costy.application.bankapi.delete_bankapi import DeleteBankAPI
from costy.application.bankapi.read_bankapi_list import ReadBankapiList
from costy.application.bankapi.update_bank_operations import UpdateBankOperations
from costy.application.category.create_category import CreateCategory
from costy.application.category.delete_category import DeleteCategory
from costy.application.category.read_available_categories import ReadAvailableCategories
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
            settings.jwks_uri, web_session, timedelta(days=1),
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
    session_maker = from_context(provides=async_sessionmaker[AS], scope=Scope.APP)
    tables = from_context(provides=dict[str, Table], scope=Scope.APP)
    auth_settings = from_context(provides=AuthSettings, scope=Scope.APP)
    banks_conf = from_context(provides=dict[str, Any], scope=Scope.APP)

    r = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AS],
    ) -> AsyncIterable[AS]:
        session = session_maker()
        yield session
        await session.close()

    @provide(scope=Scope.REQUEST)
    async def get_auth_gateway(
        self,
        session: AS,
        web_session: AsyncClient,
        tables: dict[str, Table],
        settings: AuthSettings,
    ) -> AG:
        return AG(session, web_session, tables["users"], settings)

    @provide(scope=Scope.REQUEST)
    async def get_user_gateway(
        self, session: AS, tables: dict[str, Table],
    ) -> UserAdapter:
        return UG(session, tables["users"])

    @provide(scope=Scope.REQUEST)
    async def get_operation_gateway(self, session: AS, tables: dict[str, Table]) -> OG:
        return OG(session, tables["operations"])

    @provide(scope=Scope.REQUEST)
    async def get_category_gateway(self, session: AS, tables: dict[str, Table]) -> CG:
        return CG(session, tables["categories"], tables["category_mcc"])

    @provide(scope=Scope.REQUEST)
    async def get_bank_gateways(
        self,
        web_session: AsyncClient,
        banks_conf: dict[str, Any],
    ) -> dict[str, BankAdapter]:
        return {
            "monobank": MonobankAdapter(web_session, banks_conf),
        }

    @provide(scope=Scope.REQUEST)
    async def get_bankapi_gateway(
        self,
        session: AS,
        web_session: AsyncClient,
        tables: dict[str, Table],
        bank_gateways: dict[str, BankAdapter],
        banks_conf: dict[str, Any],
    ) -> BG:
        return BG(session, web_session, tables["bankapis"], bank_gateways, banks_conf)

    @provide(scope=Scope.REQUEST)
    async def get_operation_dependencies(
        self, gateway: OG, session: AS,
    ) -> tuple[OG, AS]:
        return gateway, session

    @provide(scope=Scope.REQUEST)
    async def get_category_dependencies(
        self, gateway: CG, session: AS,
    ) -> tuple[CG, AS]:
        return gateway, session

    @provide(scope=Scope.REQUEST)
    async def get_bankapi_dependencies(self, gateway: BG, session: AS) -> tuple[BG, AS]:
        return gateway, session

    # Interactors

    @provide(scope=Scope.REQUEST)
    async def get_authenticate(self, auth_gateway: AG, session: AS) -> Authenticate:
        return Authenticate(auth_gateway, session)

    @provide
    async def get_create_user(
        self, user_gateway: UG, auth_gateway: AG, session: AS,
    ) -> CreateUser:
        return CreateUser(UserService(), user_gateway, auth_gateway, session)

    @provide
    async def get_create_operation(
        self, depends: tuple[OG, AS], idp: IDP,
    ) -> CreateOperation:
        return CreateOperation(OperationService(), depends[0], idp, depends[1])

    @provide
    async def get_read_list_operation(
        self, depends: tuple[OG, AS], idp: IDP,
    ) -> ReadListOperation:
        return ReadListOperation(OperationService(), depends[0], idp, depends[1])

    @provide
    async def get_delete_operation(
        self, depends: tuple[OG, AS], idp: IDP,
    ) -> DeleteOperation:
        return DeleteOperation(AccessService(), depends[0], idp, depends[1])

    @provide
    async def get_update_operation(
        self, depends: tuple[OG, AS], idp: IDP,
    ) -> UpdateOperation:
        return UpdateOperation(
            OperationService(), AccessService(), depends[0], idp, depends[1],
        )

    @provide
    async def get_create_category(
        self, depends: tuple[CG, AS], idp: IDP,
    ) -> CreateCategory:
        return CreateCategory(CategoryService(), depends[0], idp, depends[1])

    @provide
    async def get_delete_category(
        self, depends: tuple[CG, AS], idp: IDP,
    ) -> DeleteCategory:
        return DeleteCategory(AccessService(), depends[0], idp, depends[1])

    @provide
    async def get_update_category(
        self, depends: tuple[CG, AS], idp: IDP,
    ) -> UpdateCategory:
        return UpdateCategory(
            CategoryService(), AccessService(), depends[0], idp, depends[1],
        )

    @provide
    async def get_read_available_categories(
        self, depends: tuple[CG, AS], idp: IDP,
    ) -> ReadAvailableCategories:
        return ReadAvailableCategories(CategoryService(), depends[0], idp, depends[1])

    @provide
    async def get_create_bankapi(
        self, depends: tuple[BG, AS], idp: IDP,
    ) -> CreateBankAPI:
        return CreateBankAPI(BankAPIService(), depends[0], idp, depends[1])

    @provide
    async def get_delete_bankapi(
        self, depends: tuple[BG, AS], idp: IDP,
    ) -> DeleteBankAPI:
        return DeleteBankAPI(AccessService(), depends[0], idp, depends[1])

    @provide
    async def get_read_bankapi_list(
        self, gateway: BankAPIAdapter, idp: IdProvider,
    ) -> ReadBankapiList:
        return ReadBankapiList(gateway, idp)

    @provide
    async def get_update_bank_operations(
        self,
        depends: tuple[BG, AS],
        idp: IDP,
        operation_gateway: OperationAdapter,
        category_gateway: CategoryAdapter,
    ) -> UpdateBankOperations:
        return UpdateBankOperations(
            BankAPIService(),
            OperationService(),
            depends[0],
            operation_gateway,
            category_gateway,
            idp,
            depends[1],
        )
