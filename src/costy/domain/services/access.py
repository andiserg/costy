from typing import Protocol

from costy.domain.models.user import UserId


class HasUserId(Protocol):
    user_id: UserId


class HasOptionalUserId(Protocol):
    user_id: UserId | None


class AccessService:
    def ensure_can_edit(self, entity: HasUserId | HasOptionalUserId, user_id: UserId) -> bool:
        return entity.user_id == user_id
