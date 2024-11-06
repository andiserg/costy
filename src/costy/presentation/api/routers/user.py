from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post

from costy.application.user.create_user import CreateUser, InputData
from costy.domain.models.user import UserId


class UserController(Controller):
    path = "/users"
    tags = ("Users",)

    @post()
    @inject
    async def register(
        self,
        create_user: FromDishka[CreateUser],
        data: InputData,
    ) -> dict[str, UserId]:
        user_id = await create_user(data)
        return {"user_id": user_id}
