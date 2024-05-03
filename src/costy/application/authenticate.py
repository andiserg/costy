from dataclasses import dataclass

from .common.auth_gateway import AuthLoger
from .common.interactor import Interactor
from .common.uow import UoW


@dataclass
class LoginInputDTO:
    email: str
    password: str


class Authenticate(Interactor[LoginInputDTO, str | None]):
    def __init__(self, auth_gateway: AuthLoger, uow: UoW):
        self.auth_gateway = auth_gateway
        self.uow = uow

    async def __call__(self, data: LoginInputDTO) -> str | None:
        return await self.auth_gateway.authenticate(data.email, data.password)
