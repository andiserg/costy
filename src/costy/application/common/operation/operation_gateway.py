from abc import abstractmethod
from typing import Protocol, runtime_checkable

from costy.domain.models.operation import Operation, OperationId
from costy.domain.models.user import UserId


@runtime_checkable
class OperationReader(Protocol):
    @abstractmethod
    async def get_operation(self, operation_id: OperationId) -> Operation | None:
        raise NotImplementedError


@runtime_checkable
class OperationSaver(Protocol):
    @abstractmethod
    async def save_operation(self, operation: Operation) -> None:
        raise NotImplementedError


@runtime_checkable
class OperationsBulkSaver(Protocol):
    @abstractmethod
    async def save_operations(self, operations: list[Operation]) -> None:
        raise NotImplementedError


@runtime_checkable
class OperationsReader(Protocol):
    @abstractmethod
    async def find_operations_by_user(
        self, user_id: UserId, from_time: int | None, to_time: int | None
    ) -> list[Operation]:
        raise NotImplementedError


@runtime_checkable
class OperationDeleter(Protocol):
    @abstractmethod
    async def delete_operation(self, operation_id: OperationId) -> None:
        raise NotImplementedError


@runtime_checkable
class OperationUpdater(Protocol):
    @abstractmethod
    async def update_operation(self, operation_id: OperationId, operation: Operation) -> None:
        raise NotImplementedError
