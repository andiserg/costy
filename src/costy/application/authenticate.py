from dataclasses import dataclass

from costy.application.common.id_provider import IdProvider
from costy.application.common.interactor import Interactor
from costy.application.common.uow import UoW
from costy.domain.models.user import UserId


@dataclass
class LoginInputDTO:
    email: str
    password: str


class Authenticate(Interactor[LoginInputDTO, UserId]):
    def __init__(self, id_provider: IdProvider, uow: UoW):
        self.id_provider = id_provider
        self.uow = uow

    def __call__(self, *args, **kwargs) -> UserId:
        pass
