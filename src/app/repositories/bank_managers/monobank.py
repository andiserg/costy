from datetime import datetime, timedelta

import aiohttp

from src.app.models.operations import Operation
from src.app.services.bank_managers import BankManagerRepository


class MonobankManagerRepository(BankManagerRepository):
    __bankname__ = "monobank"
    MAX_UPDATE_PERIOD = timedelta(30)

    async def get_costs(
        self, from_time=datetime.now(), to_time=datetime.now() - MAX_UPDATE_PERIOD
    ) -> list[Operation]:
        url = "https://api.monobank.ua/personal/statement/0"
        headers = {"X-Token": self.properties["X-Token"]}
        result_operations = []
        async with aiohttp.ClientSession(headers=headers) as session:
            while from_time:
                response = await session.get(f"{url}/{from_time}/{to_time}")
                operations = await response.json()
                costs = list(filter(lambda operation: operation.amount < 0, operations))
                result_operations.append(*costs)
                from_time = operations[-1]["time"] if len(operations) == 500 else None
                # В одного запиту до Monobank API обмеження - 500 операцій
                # Тому, якщо вийшло 500 операцій то можливо, ще є операції
                # В такому випадку, потрібно зробити ще один запит
                # Від часу остальної операцій до to_time
        return [Operation(**operation) for operation in result_operations]
