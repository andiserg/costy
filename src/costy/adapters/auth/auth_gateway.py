from dataclasses import dataclass

from aiohttp import ClientSession
from sqlalchemy import Select, Table
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.auth_gateway import AuthLoger
from costy.domain.exceptions.access import AuthenticationError
from costy.domain.models.user import UserId


@dataclass
class AuthSettings:
    authorize_url: str
    client_id: str
    client_secret: str
    audience: str
    grant_type: str


class AuthGateway(AuthLoger):
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
            if response.status == 200:
                data = await response.json()
                token = data.get("access_token")
                if token:
                    return token
        raise AuthenticationError()

    async def get_user_by_sub(self, sub: str) -> UserId:
        query = Select(self.table).where(self.table.c.auth_id == sub)
        result = await self.db_session.execute(query)
        return tuple(result)[0][0]
