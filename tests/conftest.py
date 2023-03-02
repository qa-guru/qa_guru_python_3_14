import os

import pytest
from dotenv import load_dotenv

from utils.base_session import BaseSession


load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--env")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def demoshop():
    api_url = os.getenv("API_URL")
    return BaseSession(api_url)


@pytest.fixture(scope="session")
def reqres():
    api_url = "https://reqres.in"
    return BaseSession(api_url)
