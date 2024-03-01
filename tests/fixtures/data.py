import os

import pytest
from pytest_asyncio import fixture

from costy.application.authenticate import LoginInputDTO
from costy.application.category.dto import NewCategoryDTO
from costy.application.operation.dto import NewOperationDTO
from costy.application.user.dto import NewUserDTO
from costy.domain.models.category import Category, CategoryId
from costy.domain.models.operation import Operation, OperationId
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


# global is used because tests cannot use a "session" fixed fixture in this case
user_token_state = None


@fixture
async def user_token(auth_adapter, credentials):  # type: ignore
    global user_token_state
    if not user_token_state:
        response = await auth_adapter.authenticate(credentials["username"], credentials["password"])
        if response:
            return response
        pytest.fail("Failed to test user authenticate.")
    else:
        return user_token_state


@fixture
async def auth_sub() -> str:  # type: ignore
    try:
        return os.environ["TEST_AUTH_USER_SUB"].replace("auth|0", "")
    except KeyError:
        pytest.fail("No test user sub environment variable.")


@fixture
async def credentials() -> dict[str, str]:  # type: ignore
    try:
        return {
            "username": os.environ["TEST_AUTH_USER"],
            "password": os.environ["TEST_AUTH_PASSWORD"]
        }
    except KeyError:
        pytest.fail("No test user credentials.")


@fixture
async def operation_list(user_id, category_id):
    return [
        Operation(
            id=0,
            user_id=user_id,
            amount=100,
            description="test description",
            category_id=category_id,
            time=1111
        ),
        Operation(
            id=1,
            user_id=user_id,
            amount=100,
            description="test description",
            category_id=category_id,
            time=1111
        ),
        Operation(
            id=2,
            user_id=user_id,
            amount=100,
            description="test description",
            category_id=category_id,
            time=1111
        ),
        Operation(
            id=3,
            user_id=user_id,
            amount=100,
            description="test description",
            category_id=category_id,
            time=1111
        )
    ]


@fixture
async def category_list(user_id):
    return [
        Category(id=0, name="test", user_id=user_id),
        Category(id=1, name="test", user_id=user_id),
        Category(id=2, name="test", user_id=user_id),
    ]
