from datetime import timedelta
from typing import AsyncIterable

from dishka import AnyOf, Provider, Scope, from_context, provide
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from auth.adapters.auth_gateway import AuthAdapter
from auth.adapters.token import JwtTokenProcessor, KeySetProvider, TokenUserProvider
from auth.adapters.user_gateway import UserAdapter
from auth.application._common import (
    AuthLoger,
    AuthRegister,
    Commiter,
    UserProvider,
    UserReader,
    UserSaver,
)
from auth.application.authenticate import Authenticate
from auth.application.create_user import CreateUser
from auth.application.get_user import GetUser
from auth.config import AuthSettings


class DIProvider(Provider):
    scope = Scope.REQUEST

    web_session = from_context(provides=AsyncClient, scope=Scope.APP)
    session_maker = from_context(
        provides=async_sessionmaker[AsyncSession], scope=Scope.APP,
    )
    auth_settings = from_context(provides=AuthSettings, scope=Scope.APP)

    auth_gateway = provide(
        source=AuthAdapter,
        provides=AnyOf[AuthLoger, AuthRegister],
    )
    user_gateway = provide(
        source=UserAdapter,
        provides=AnyOf[UserSaver, UserReader],
    )

    @provide
    async def session(
            self,
            session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, Commiter]]:
        async with session_maker() as session:
            yield session

    @provide
    async def user_provider(
        self,
        session: AsyncClient,
        settings: AuthSettings,
        user_gateway: UserReader,
    ) -> UserProvider:
        jwt_processor = JwtTokenProcessor(
            algorithm="RS256",
            audience=settings.audience,
            issuer=settings.issuer,
        )

        key_set_provider = KeySetProvider(
            settings.jwks_uri,
            session,
            timedelta(days=1),
        )
        return TokenUserProvider(jwt_processor, key_set_provider, user_gateway)

    get_authenticate = provide(Authenticate)
    get_create_user = provide(CreateUser)
    get_get_user = provide(GetUser)
