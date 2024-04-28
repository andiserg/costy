import logging

from httpx import AsyncClient
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.auth_gateway import AuthLoger, AuthRegister
from costy.domain.exceptions.access import AuthenticationError, RegisterError
from costy.infrastructure.config import AuthSettings

logger = logging.getLogger(__name__)


class AuthGateway(AuthLoger, AuthRegister):
    AUTH_SUCCESS_CODE = 200
    REGISTER_SUCCESS_CODE = 200

    def __init__(
        self,
        db_session: AsyncSession,
        web_session: AsyncClient,
        table: Table,
        settings: AuthSettings,
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
            "grant_type": self.settings.grant_type,
        }
        response = await self.web_session.post(url, data=data)
        response_data = response.json()
        if response.status_code == self.AUTH_SUCCESS_CODE:
            token: str | None = response_data.get("access_token")
            if token:
                return token
        logger.info("Authentication failed: %s", response_data)
        raise AuthenticationError(response_data)

    async def register(self, email: str, password: str) -> str:
        url = self.settings.register_url
        data = {
            "email": email,
            "password": password,
            "client_id": self.settings.client_id,
            "client_secret": self.settings.client_secret,
            "connection": self.settings.connection,
        }
        response = await self.web_session.post(url, data=data)
        response_data = response.json()
        if response.status_code == self.REGISTER_SUCCESS_CODE:
            return response_data["_id"]
        logger.info("Register failed: %s", response_data)
        raise RegisterError(response_data)
