from typing import TypeVar, Generic

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class Interactor(Generic[InputDTO, OutputDTO]):
    def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError
