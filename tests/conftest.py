import pytest
import requests

def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru",
        help="This is request url"
    )

    parser.addoption(
        "--status_code",
        default=200,
        help="This is status_code from request to url"
    )

@pytest.fixture()
def request_to_url(request):
    return requests.get(request.config.getoption("--url"))

@pytest.fixture
def status_code(request):
    return int(request.config.getoption("--status_code"))

@pytest.fixture
def request_get():
    return requests.get

@pytest.fixture
def request_method(method, target):
    return getattr(requests, method)(url=target)
