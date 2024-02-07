from abc import abstractmethod
from typing import Any, Generic, Type, TypeVar

ObjectType = TypeVar("ObjectType")


class Converter(Generic[ObjectType]):
    @abstractmethod
    def load(self, data: dict, tp: Type[ObjectType]) -> ObjectType:
        raise NotImplementedError

    @abstractmethod
    def dump(self, tp: ObjectType):
        raise NotImplementedError

    @abstractmethod
    def convert(self, tp1: Any, tp2: Type[ObjectType]) -> ObjectType:
        raise NotImplementedError
