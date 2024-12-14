from typing import Protocol


class HasUserId(Protocol):
    user_id: int


class HasOptionalUserId(Protocol):
    user_id: int | None


class AccessService:
    def ensure_can_edit(
        self,
        entity: HasUserId | HasOptionalUserId,
        user_id: int,
    ) -> bool:
        return entity.user_id == user_id
