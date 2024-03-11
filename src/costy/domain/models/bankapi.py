from dataclasses import dataclass
from typing import NewType

from costy.domain.models.user import UserId

BankApiId = NewType("BankApiId", int)


@dataclass(kw_only=True)
class BankAPI:
    id: BankApiId | None = None
    name: str
    access_data: dict
    updated_at: int | None
    user_id: UserId
