from dataclasses import dataclass

from auth.application._common import Interactor, UserProvider
from auth.exceptions import AuthenticationError
from auth.models import User


@dataclass(slots=True)
class InputData:
    token: str


class GetUser(Interactor[InputData, User]):
    def __init__(self, user_provider: UserProvider) -> None:
        self.user_provider = user_provider

    async def __call__(self, data: InputData) -> User:
        if not data.token:
            raise AuthenticationError("Invalid token")

        return await self.user_provider.get_user_by_token(data.token)
