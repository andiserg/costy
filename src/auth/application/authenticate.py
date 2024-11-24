from dataclasses import dataclass

from ._common import AuthLoger, Commiter, Interactor


@dataclass
class InputData:
    email: str
    password: str


class Authenticate(Interactor[InputData, str | None]):
    def __init__(self, auth_gateway: AuthLoger, uow: Commiter) -> None:
        self.auth_gateway = auth_gateway
        self.uow = uow

    async def __call__(self, data: InputData) -> str | None:
        return await self.auth_gateway.authenticate(data.email, data.password)
