from costy.domain.models.category import CategoryId
from costy.domain.models.operation import Operation
from costy.domain.models.user import UserId
from costy.domain.sentinel import Sentinel


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

    def update(
        self,
        operation: Operation,
        amount: int | type[Sentinel] = Sentinel,
        description: str | None | type[Sentinel] = Sentinel,
        time: int | type[Sentinel] = Sentinel,
        category_id: CategoryId | type[Sentinel] = Sentinel,
    ):
        exclude_params = ['self', 'operation', 'exclude_params']
        params = {
            name: value for name, value in locals().items()
            if value is not Sentinel and name not in exclude_params
        }
        for name, value in params.items():
            setattr(operation, name, value)
