from costy.domain.models.category import Category, CategoryId
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
        amount: int | None = None,
        description: str | None | type[Sentinel] = Sentinel,
        time: int | None = None,
        category_id: CategoryId | None | type[Sentinel] = Sentinel,
    ):
        exclude_params = ('self', 'operation', 'exclude_params', 'sentinel_params')
        sentinel_params = ('description', 'category_id')
        params = {
            name: value for name, value in locals().items() if
            (name not in exclude_params) and
            (
                (name in sentinel_params and value is not Sentinel) or
                (name not in sentinel_params and value is not None)
            )

        }
        for name, value in params.items():
            setattr(operation, name, value)

    def set_category(self, operation: Operation, category: Category) -> None:
        operation.category_id = category.id  # type: ignore
