import os

import pytest
from dotenv import load_dotenv

from utils.base_session import BaseSession


load_dotenv()


@pytest.fixture(scope="session")
def demoshop():
    api_url = os.getenv("API_URL")
    return BaseSession(api_url)
