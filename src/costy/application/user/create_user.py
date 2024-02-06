from dataclasses import dataclass

from costy.domain.models.user import UserId
from costy.domain.services.user import UserService

from ..common.interactor import Interactor
from ..common.uow import UoW
from ..common.user_gateway import UserSaver


@dataclass
class NewUserDTO:
    email: str
    password: str


class CreateUser(Interactor[NewUserDTO, UserId]):
    def __init__(
        self,
        user_service: UserService,
        user_db_gateway: UserSaver,
        uow: UoW,
    ):
        self.user_service = user_service
        self.user_db_gateway = user_db_gateway
        self.uow = uow

    async def __call__(self, data: NewUserDTO) -> UserId:
        user = self.user_service.create(data.email, data.password)
        await self.user_db_gateway.save_user(user)
        user_id = user.id
        await self.uow.commit()
        return user_id  # type: ignore
