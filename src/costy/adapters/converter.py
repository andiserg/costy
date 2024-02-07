from typing import Any, Type, Union

from adaptix import Retort

from costy.application.common.converter import Converter, ObjectType


class AdaptixConverter(Converter[ObjectType]):
    def __init__(self, retort: Retort):
        self.retort = retort

    def load(self, data: dict, tp: Type[ObjectType]) -> ObjectType:
        return self.retort.load(data, tp)

    def dump(self, tp: ObjectType) -> dict:
        return self.retort.dump(tp)

    def convert(self, tp1: Any, tp2: Type[ObjectType]) -> ObjectType:
        if isinstance(tp1, list):
            elems_type: Union[Any] = Union[tuple(type(elem) for elem in tp1)]
            dumped: dict = self.retort.dump(tp1, list[elems_type])
        else:
            dumped = self.retort.dump(tp1)
        return self.retort.load(dumped, tp2)
