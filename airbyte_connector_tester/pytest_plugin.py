import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--my-option", action="store", default="default", help="My custom pytest option"
    )


@pytest.fixture
def my_fixture(request):
    return request.config.getoption("--my-option")


def pytest_runtest_setup(item):
    # This hook is called before each test function is executed
    print(f"Setting up test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    # This hook is called after each test function is executed
    print(f"Tearing down test: {item.name}")
