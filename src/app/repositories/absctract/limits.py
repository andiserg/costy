from abc import abstractmethod

from src.app.repositories.absctract.base import AbstractRepository


class ALimitRepository(AbstractRepository):
    @abstractmethod
    async def get_all(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError
