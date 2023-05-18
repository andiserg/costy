import json
import os
from datetime import datetime, timedelta

from src.app.repositories.absctract.bank_api import ABankManagerRepository


class FakeBankManagerRepository(ABankManagerRepository):
    __bankname__ = "fake_bank"
    MAX_UPDATE_PERIOD = (
        datetime.now() - datetime.fromtimestamp(1683274878) + timedelta(days=1)
    )  # На 1 день раніше найстарішої операції в cost.json

    async def get_costs(self, from_time=None, to_time=None) -> list[dict]:
        if not from_time:
            from_time = int((datetime.now() - self.MAX_UPDATE_PERIOD).timestamp())
        if not to_time:
            to_time = int(datetime.now().timestamp())

        costs = self._get_costs_by_json()
        filtered_costs = list(
            filter(lambda cost: from_time < cost["time"] < to_time, costs)
        )

        for cost in filtered_costs:
            cost["user_id"] = self.properties["user_id"]
            cost["bank_name"] = self.__bankname__
            cost["source_type"] = "fake_bank"
        return filtered_costs

    def _get_costs_by_json(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "costs.json")
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
