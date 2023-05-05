from datetime import datetime, timedelta

import aiohttp

from src.app.domain.operations import Operation
from src.app.services.bank_api import ABankManagerRepository


class MonobankManagerRepository(ABankManagerRepository):
    __bankname__ = "monobank"
    MAX_UPDATE_PERIOD = timedelta(30)

    async def get_costs(self, from_time=None, to_time=None) -> list[Operation]:
        if not from_time:
            from_time = int((datetime.now() - self.MAX_UPDATE_PERIOD).timestamp())
        if not to_time:
            to_time = int(datetime.now().timestamp())

        url = "https://api.monobank.ua/personal/statement/0"
        headers = {"X-Token": self.properties["X-Token"]}
        result_operations = []

        async with aiohttp.ClientSession(headers=headers) as session:
            while from_time:
                response = await session.get(f"{url}/{from_time}/{to_time}")
                operations = await response.json()
                if not operations:
                    return []
                if "errorDescription" in operations:
                    return None
                costs = self.validate_operations(operations)
                result_operations += costs
                from_time = operations[-1]["time"] if len(operations) == 500 else None
                # В одного запиту до Monobank API обмеження - 500 операцій
                # Тому, якщо вийшло 500 операцій то можливо, ще є операції
                # В такому випадку, потрібно зробити ще один запит
                # Від часу остальної операцій до to_time

        return [
            Operation(
                **operation,
                user_id=self.properties["user_id"],
                source_type=self.properties["bank_name"],
            )
            for operation in result_operations
        ]

    def validate_operations(self, operations: list[dict]) -> list[dict]:
        costs = list(filter(lambda operation: operation["amount"] < 0, operations))
        for cost in costs:
            cost["amount"] *= -1
            # Сума витрати в програмі оперуються як додатні величини
            del cost["id"]
            # Видалення id з операції, яке йому надає monobank
        return costs
