from dataclasses import dataclass
from typing import NewType

UserId = NewType("UserId", int)


@dataclass(slots=True, kw_only=True)
class User:
    id: UserId | None = None
    auth_id: str | None = None
