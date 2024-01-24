from abc import abstractmethod
from typing import Protocol

from costy.domain.models.operation import Operation, OperationId
from costy.domain.models.user import UserId


class OperationReader(Protocol):
    @abstractmethod
    async def get_operation(self, operation_id: OperationId) -> Operation:
        raise NotImplementedError


class OperationSaver(Protocol):
    @abstractmethod
    async def save_operation(self, operation: Operation) -> None:
        raise NotImplementedError


class OperationsReader(Protocol):
    @abstractmethod
    async def find_operations_by_user_id(
        self, user_id: UserId, from_time: int, to_time: int
    ) -> list[Operation]:
        raise NotImplementedError


class OperationDeleter(Protocol):
    @abstractmethod
    async def delete_operation(self, operation_id: OperationId) -> None:
        raise NotImplementedError
