from dataclasses import dataclass

from costy.domain.models.operation import Operation


@dataclass
class CreateBankApiDTO:
    name: str
    access_data: dict


@dataclass(kw_only=True)
class BankOperationDTO:
    operation: Operation
    mcc: int
