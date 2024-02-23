from aiohttp import ClientSession
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.auth_gateway import AuthLoger, AuthRegister
from costy.domain.exceptions.access import AuthenticationError, RegisterError
from costy.infrastructure.config import AuthSettings


class AuthGateway(AuthLoger, AuthRegister):

    def __init__(
        self,
        db_session: AsyncSession,
        web_session: ClientSession,
        table: Table,
        settings: AuthSettings
    ) -> None:
        self.db_session = db_session
        self.web_session = web_session
        self.table = table
        self.settings = settings

    async def authenticate(self, email: str, password: str) -> str:
        url = self.settings.authorize_url
        data = {
            "username": email,
            "password": password,
            "client_id": self.settings.client_id,
            "client_secret": self.settings.client_secret,
            "audience": self.settings.audience,
            "grant_type": self.settings.grant_type
        }
        async with self.web_session.post(url, data=data) as response:
            response_data = await response.json()
            if response.status == 200:
                token: str | None = response_data.get("access_token")
                if token:
                    return token
            raise AuthenticationError(response_data)

    async def register(self, email: str, password: str) -> str:
        url = self.settings.register_url
        data = {
            "email": email,
            "password": password,
            "client_id": self.settings.client_id,
            "client_secret": self.settings.client_secret,
            "connection": self.settings.connection
        }
        async with self.web_session.post(url, data=data) as response:
            response_data = await response.json()
            if response.status == 200:
                return response_data["_id"]
            raise RegisterError(response_data)
