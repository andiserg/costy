from abc import abstractmethod
from datetime import datetime
from typing import Protocol

from costy.application.common.bankapi.dto import BankOperationDTO
from costy.domain.models.user import UserId


class BankGateway(Protocol):
    @abstractmethod
    async def fetch_operations(
        self,
        access_data: dict,
        user_id: UserId,
        from_time: datetime | None = None,
    ) -> list[BankOperationDTO] | None:
        raise NotImplementedError
