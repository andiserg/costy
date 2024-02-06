from dataclasses import dataclass

from costy.application.common.interactor import Interactor
from costy.application.common.uow import UoW
from costy.application.common.user_gateway import UserReader
from costy.domain.models.user import UserId


@dataclass
class LoginInputDTO:
    email: str
    password: str


class Authenticate(Interactor[LoginInputDTO, UserId | None]):
    def __init__(self, user_gateway: UserReader, uow: UoW):
        self.user_gateway = user_gateway
        self.uow = uow

    async def __call__(self, data: LoginInputDTO) -> UserId | None:
        user = await self.user_gateway.get_user_by_email(data.email)
        # TODO: compare hashed passwords
        return user.id if user else None
