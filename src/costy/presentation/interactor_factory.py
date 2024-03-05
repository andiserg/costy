from abc import ABC, abstractmethod
from typing import AsyncContextManager

from costy.application.authenticate import Authenticate
from costy.application.category.create_category import CreateCategory
from costy.application.category.delete_category import DeleteCategory
from costy.application.category.read_available_categories import (
    ReadAvailableCategories,
)
from costy.application.category.update_category import UpdateCategory
from costy.application.common.id_provider import IdProvider
from costy.application.operation.create_operation import CreateOperation
from costy.application.operation.delete_operation import DeleteOperation
from costy.application.operation.read_list_operation import ReadListOperation
from costy.application.operation.update_operation import UpdateOperation
from costy.application.user.create_user import CreateUser


class InteractorFactory(ABC):
    @abstractmethod
    def authenticate(self) -> AsyncContextManager[Authenticate]:
        pass

    @abstractmethod
    def create_user(self) -> AsyncContextManager[CreateUser]:
        pass

    @abstractmethod
    def create_operation(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[CreateOperation]:
        pass

    @abstractmethod
    def read_list_operation(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[ReadListOperation]:
        pass

    @abstractmethod
    def delete_operation(
            self, id_provider: IdProvider
    ) -> AsyncContextManager[DeleteOperation]:
        pass

    @abstractmethod
    def update_operation(
            self, id_provider: IdProvider
    ) -> AsyncContextManager[UpdateOperation]:
        pass

    @abstractmethod
    def create_category(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[CreateCategory]:
        pass

    @abstractmethod
    def delete_category(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[DeleteCategory]:
        pass

    @abstractmethod
    def update_category(
            self, id_provider: IdProvider
    ) -> AsyncContextManager[UpdateCategory]:
        pass

    @abstractmethod
    def read_available_categories(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[ReadAvailableCategories]:
        pass
