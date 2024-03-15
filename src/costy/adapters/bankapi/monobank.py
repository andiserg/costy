from datetime import datetime, timedelta

from adaptix import P, Retort, loader
from httpx import AsyncClient

from costy.adapters.bankapi.bank_gateway import BankGateway
from costy.application.common.bankapi.dto import BankOperationDTO
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.operation import Operation
from costy.domain.models.user import UserId


class MonobankGateway(BankGateway):
    def __init__(
        self,
        web_session: AsyncClient,
        bank_conf: dict,
        retort: Retort
    ):
        self._web_session = web_session
        self._bank_conf = bank_conf["monobank"]
        self._retort = retort.extend(recipe=[loader(P[Operation].id, lambda _: None)])

    async def fetch_operations(
        self,
        access_data: dict,
        user_id: UserId,
        from_time: datetime | None = None
    ) -> list[BankOperationDTO]:
        to_time = datetime.now()
        if not from_time:
            from_time = datetime.now() - timedelta(days=31)
        elif from_time > to_time:
            raise InvalidRequestError("Parameter to_time must be greater than from_time")

        from_time = int(from_time.timestamp())  # type: ignore
        to_time = int(to_time.timestamp())  # type: ignore

        total_operations = []
        while from_time:
            url = f"{self._bank_conf['url']}/{from_time}/{to_time}"
            response = await self._web_session.get(url, headers=access_data)
            operations = response.json()
            total_operations.extend(operations)
            # The maximum operation limit in response is 500 items
            from_time = operations[-1]["time"] if len(operations) == 500 else None

        for operation in total_operations:
            operation["user_id"] = user_id
            operation["bank_name"] = "monobank"

        loaded_operations = self._retort.load(total_operations, list[Operation])
        return [
            BankOperationDTO(operation=loaded_operation, mcc=operation["mcc"])
            for loaded_operation, operation in zip(loaded_operations, total_operations)
        ]
