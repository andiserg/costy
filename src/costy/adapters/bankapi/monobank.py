import logging
from datetime import datetime, timedelta

from adaptix import P, Retort, loader
from httpx import AsyncClient

from costy.adapters.bankapi.bank_gateway import BankGateway
from costy.application.common.bankapi.dto import BankOperationDTO
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.operation import Operation
from costy.domain.models.user import UserId

logger = logging.getLogger("bankAPI: " + __name__)


class MonobankGateway(BankGateway):
    SUCCESS_CODE = 200
    FAILED_CODE = 403
    OPERATION_LIMIT = 500

    def __init__(
        self,
        web_session: AsyncClient,
        bank_conf: dict,
        retort: Retort,
    ):
        self._web_session = web_session
        self._bank_conf = bank_conf["monobank"]
        self._retort = retort.extend(recipe=[loader(P[Operation].id, lambda _: None)])

    async def fetch_operations(
        self,
        access_data: dict,
        user_id: UserId,
        from_time: datetime | None = None,
    ) -> list[BankOperationDTO] | None:
        to_time = datetime.now()
        from_time = from_time or datetime.now() - timedelta(days=31)

        if from_time > to_time:
            raise InvalidRequestError("Parameter to_time must be greater than from_time")

        from_time = int(from_time.timestamp())  # type: ignore[assignment]
        to_time = int(to_time.timestamp())  # type: ignore[assignment]

        total_operations = []
        while to_time:
            url = f"{self._bank_conf['url']}/{from_time}/{to_time}"
            response = await self._web_session.get(url, headers=access_data)

            if response.status_code == self.FAILED_CODE:
                logger.warning(
                    "Monobank API token failed: url: %s, response: %s",
                    url,
                    response.text,
                )
                return None

            if response.status_code != self.SUCCESS_CODE:
                logger.error(
                    "Monobank API unknown failed: url: %s, response: %s",
                    url,
                    response.text,
                )
                return None

            operations = response.json()
            total_operations.extend(operations)

            # The maximum operation limit in response is 500 items
            to_time = operations[-1]["time"] if len(operations) == self.OPERATION_LIMIT else None

        for operation in total_operations:
            operation["user_id"] = user_id
            operation["bank_name"] = "monobank"

        loaded_operations = self._retort.load(total_operations, list[Operation])
        return [
            BankOperationDTO(operation=loaded_operation, mcc=operation["mcc"])
            for loaded_operation, operation in zip(loaded_operations, total_operations)
        ]
