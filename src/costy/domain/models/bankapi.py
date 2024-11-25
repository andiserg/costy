from dataclasses import dataclass
from typing import NewType

BankApiId = NewType("BankApiId", int)


@dataclass(slots=True, kw_only=True)
class BankAPI:
    id: BankApiId | None = None
    name: str
    access_data: dict[str, str]
    updated_at: int | None = None
    user_id: int
