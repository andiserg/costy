from litestar import Controller, post

from costy.application.common.user.dto import NewUserDTO
from costy.domain.models.user import UserId
from costy.presentation.interactor_factory import InteractorFactory


class UserController(Controller):
    path = "/users"
    tags = ("Users",)

    @post()
    async def register(self, ioc: InteractorFactory, data: NewUserDTO) -> dict[str, UserId]:
        async with ioc.create_user() as create_user:
            user_id = await create_user(data)
        return {"user_id": user_id}
