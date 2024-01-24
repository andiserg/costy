from dataclasses import dataclass

from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.user_gateway import UserSaver
from ..common.uow import UoW
from costy.domain.models.user import UserId
from costy.domain.services.user import UserService


@dataclass
class NewUserDTO:
    email: str
    password: str


class CreateUser(Interactor[NewUserDTO, UserId]):
    def __init__(
        self,
        user_service: UserService,
        user_db_gateway: UserSaver,
        id_provider: IdProvider,
        uow: UoW,
    ):
        self.user_service = user_service
        self.user_db_gateway = user_db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: NewUserDTO) -> UserId:
        user = self.user_service.create(data.email, data.password)
        await self.user_db_gateway.save_user(user)
        await self.uow.commit()
        return user.id
