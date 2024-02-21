from dataclasses import dataclass
from typing import NewType

UserId = NewType("UserId", int)


@dataclass
class User:
    id: UserId | None
