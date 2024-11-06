from abc import abstractmethod
from datetime import datetime
from typing import Protocol

from costy.application.common.bankapi_gateway import BankOperation
from costy.domain.models.user import UserId


class BankAdapter(Protocol):
    @abstractmethod
    async def fetch_operations(
        self,
        access_data: dict[str, str],
        user_id: UserId,
        from_time: datetime | None = None,
    ) -> list[BankOperation] | None:
        raise NotImplementedError
