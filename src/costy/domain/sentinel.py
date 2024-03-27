from typing import TypeAlias, TypeVar


class Sentinel:
    pass


ParamT = TypeVar("ParamT", contravariant=True)
SentinelOptional: TypeAlias = ParamT | None | type[Sentinel]
