from costy.application.common.id_provider import IdProvider
from costy.domain.exceptions.access import AuthenticationError


class TokenIdProvider(IdProvider):
    def __init__(self, token: str) -> None:
        self.token = token

    async def get_current_user_id(self) -> int:
        if not self.token:
            raise AuthenticationError("UserId not found")
        return int(self.token)
