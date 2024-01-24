from costy.domain.models.category import CategoryId
from costy.domain.models.operation import Operation
from costy.domain.models.user import UserId


class OperationService:
    def create(
        self,
        amount: int,
        description: str | None,
        time: int,
        user_id: UserId,
        category_id: CategoryId,
    ) -> Operation:
        return Operation(
            id=None,
            amount=amount,
            description=description,
            time=time,
            user_id=user_id,
            category_id=category_id,
        )
