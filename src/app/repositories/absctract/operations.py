from abc import abstractmethod

from src.app.domain.operations import Operation
from src.app.repositories.absctract.base import AbstractRepository


class AOperationRepository(AbstractRepository):
    @abstractmethod
    async def get(self, **kwargs) -> Operation:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user(
        self, user_id, from_time: int, to_time: int
    ) -> list[Operation]:
        raise NotImplementedError
