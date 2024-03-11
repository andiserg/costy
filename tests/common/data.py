import os

import pytest
from pytest_asyncio import fixture

from costy.application.authenticate import LoginInputDTO
from costy.application.common.category.dto import NewCategoryDTO
from costy.application.common.operation.dto import NewOperationDTO
from costy.application.common.user.dto import NewUserDTO
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


@fixture(scope="session")
async def auth_sub() -> str:  # type: ignore
    try:
        return os.environ["TEST_AUTH_USER_SUB"].replace("auth0|", "")
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
