from dataclasses import dataclass
from typing import NewType

UserId = NewType("UserId", int)


@dataclass(slots=True)
class User:
    id: UserId | None
    auth_id: str | None
