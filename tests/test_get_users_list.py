import logging

import requests
from pytest_voluptuous import S

from schemas.user import users_list_schema


def test_get_users_list_schema():
    result = requests.get("https://reqres.in/api/users", params={"page": 2})

    assert S(users_list_schema) == result.json()


def test_users_default_count_on_page():
    """Проверка дефолтного количества пользователей на странице."""

    response = requests.get("https://reqres.in/api/users", params={"page": 1})
    per_page = response.json()["per_page"]
    data = response.json()["data"]

    assert per_page == 6
    assert len(data) == 6
