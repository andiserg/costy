from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from costy.application.common.bankapi_gateway import Operation
from costy.domain.models.user import UserId


@dataclass
class MCCBankOperation:
    operation: Operation
    mcc: int


class BankAdapter(Protocol):
    @abstractmethod
    async def fetch_operations(
        self,
        access_data: dict[str, str],
        user_id: UserId,
        from_time: datetime | None = None,
    ) -> list[MCCBankOperation] | None:
        raise NotImplementedError
