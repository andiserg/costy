from datetime import datetime, timedelta
from itertools import chain

import aiohttp

from src.app.services.bank_api import ABankManagerRepository


class MonobankManagerRepository(ABankManagerRepository):
    __bankname__ = "monobank"
    MAX_UPDATE_PERIOD = timedelta(30)

    async def get_costs(self, from_time=None, to_time=None) -> list[dict] | None:
        from_time, to_time = self._normalize_time_values(from_time, to_time)

        operations = list(
            chain.from_iterable(self._send_request_to_api(from_time, to_time))
        )
        if not operations:
            return []
        if "errorDescription" in operations:
            return None
        costs = self.validate_operations(operations)

        for opeation in costs:
            opeation["user_id"] = self.properties["user_id"]
            opeation["bank_name"] = self.properties["bank_name"]
            opeation["source_type"] = "monobank"
        return costs

    def _normalize_time_values(self, from_time, to_time):
        """Якщо аргументи None - створення дефолтних значень"""
        if not from_time:
            from_time = int((datetime.now() - self.MAX_UPDATE_PERIOD).timestamp())
        if not to_time:
            to_time = int(datetime.now().timestamp())
        return from_time, to_time

    async def _send_request_to_api(self, from_time, to_time) -> list[dict]:
        url = "https://api.monobank.ua/personal/statement/0"
        headers = {"X-Token": self.properties["X-Token"]}
        async with aiohttp.ClientSession(headers=headers) as session:
            while from_time:
                response = await session.get(f"{url}/{from_time}/{to_time}")
                operations = await response.json()
                yield operations
                from_time = operations[-1]["time"] if len(operations) == 500 else None
                # В одного запиту до Monobank API обмеження - 500 операцій
                # Тому, якщо вийшло 500 операцій то можливо, ще є операції
                # В такому випадку, потрібно зробити ще один запит
                # Від часу остальної операцій до to_time

    def validate_operations(self, operations: list[dict]) -> list[dict]:
        """Фільтрація витрат та заміна мінусових значень amount на додатні"""
        costs = list(filter(lambda operation: operation["amount"] < 0, operations))
        for cost in costs:
            cost["amount"] *= -1
            # Сума витрати в програмі оперуються як додатні величини
            del cost["id"]
            # Видалення id з операції, яке йому надає monobank
        return costs
