from litestar import Controller, post

from costy.application.common.id_provider import IdProvider
from costy.application.user.create_user import NewUserDTO
from costy.presentation.interactor_factory import InteractorFactory


class UserController(Controller):
    path = "/users"

    @post()
    async def register(self, ioc: InteractorFactory, id_provider: IdProvider, data: NewUserDTO) -> dict:
        async with ioc.create_user(id_provider) as create_user:
            user_id = await create_user(data)
        return {"user_id": user_id}
