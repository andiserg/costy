from costy.application.common.id_provider import IdProvider
from costy.domain.models.user import UserId


class SimpleIdProvider(IdProvider):
    def __init__(self, user_id: UserId):
        self.user_id = user_id

    async def get_current_user_id(self) -> UserId:
        return self.user_id
