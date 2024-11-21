from datetime import UTC, datetime

from costy.domain.models.bankapi import BankAPI
from costy.domain.models.user import UserId


class BankAPIService:
    def create(
        self,
        bank_name: str,
        access_data: dict[str, str],
        user_id: UserId,
    ) -> BankAPI:
        return BankAPI(
            name=bank_name,
            access_data=access_data,
            updated_at=None,
            user_id=user_id,
        )

    def update_time(self, bankapi: BankAPI) -> None:
        bankapi.updated_at = int(datetime.now(tz=UTC).timestamp())
