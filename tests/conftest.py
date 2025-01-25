import pytest

pytest_plugins = [
    "tests.common.fixtures.adapters",
    "tests.common.fixtures.infrastructure",
    "tests.common.fixtures.data",
    "tests.common.fixtures.app",
    "tests.common.fixtures.env",
]

def pytest_addoption(parser):
    parser.addoption("--module", action="store")


@pytest.fixture(scope="session")
def module(pytestconfig):
    return pytestconfig.getoption("module")
