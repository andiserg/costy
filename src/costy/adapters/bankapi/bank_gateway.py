from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from costy.domain.models.operation import Operation


@dataclass
class MCCBankOperation:
    operation: Operation
    mcc: int


class BankAdapter(Protocol):
    @abstractmethod
    async def fetch_operations(
        self,
        access_data: dict[str, str],
        user_id: int,
        from_time: datetime | None = None,
    ) -> list[MCCBankOperation] | None:
        raise NotImplementedError
