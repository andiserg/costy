from typing import TypeAlias, TypeVar


class Sentinel:
    pass


ParamT_contra = TypeVar("ParamT_contra", contravariant=True)
SentinelOptional: TypeAlias = ParamT_contra | None | type[Sentinel]
