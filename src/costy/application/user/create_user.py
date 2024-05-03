from ...domain.models.user import UserId
from ...domain.services.user import UserService
from ..common.auth_gateway import AuthRegister
from ..common.interactor import Interactor
from ..common.uow import UoW
from ..common.user.dto import NewUserDTO
from ..common.user.user_gateway import UserSaver


class CreateUser(Interactor[NewUserDTO, UserId]):
    def __init__(
        self,
        user_service: UserService,
        user_db_gateway: UserSaver,
        auth_gateway: AuthRegister,
        uow: UoW,
    ):
        self.user_service = user_service
        self.user_db_gateway = user_db_gateway
        self.auth_gateway = auth_gateway
        self.uow = uow

    async def __call__(self, data: NewUserDTO) -> UserId:
        auth_id = await self.auth_gateway.register(data.email, data.password)
        user = self.user_service.create(auth_id)
        await self.user_db_gateway.save_user(user)
        user_id = user.id
        await self.uow.commit()
        return user_id  # type: ignore[return-value]
