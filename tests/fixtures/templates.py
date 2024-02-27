from pytest_asyncio import fixture

from costy.application.authenticate import LoginInputDTO
from costy.application.category.dto import NewCategoryDTO
from costy.application.operation.dto import NewOperationDTO
from costy.application.user.dto import NewUserDTO
from costy.domain.models.category import CategoryId
from costy.domain.models.operation import OperationId
from costy.domain.models.user import User, UserId


@fixture
async def user_id() -> UserId:
    return UserId(999)


@fixture
async def operation_id() -> OperationId:
    return OperationId(999)


@fixture
async def category_id() -> CategoryId:
    return CategoryId(999)


@fixture
async def user_entity() -> User:
    return User(id=None, auth_id="auth_id")


@fixture
async def category_info() -> NewCategoryDTO:
    return NewCategoryDTO("test")


@fixture
async def operation_info() -> NewOperationDTO:
    return NewOperationDTO(
        amount=100,
        description="description",
        time=10000,
        category_id=CategoryId(999)
    )


@fixture
async def user_info() -> NewUserDTO:
    return NewUserDTO(email="test@email.com", password="password")


@fixture
async def login_info() -> LoginInputDTO:
    return LoginInputDTO(email="test@email.com", password="password")


@fixture
async def token() -> str:
    return "token"


@fixture
async def auth_id() -> str:
    return "auth_id"
