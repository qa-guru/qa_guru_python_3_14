import os
from time import sleep

import allure
import requests
from allure_commons._allure import step
from selene import have
from selene.support.shared import browser
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from framework.demoqa import DemoQA
from framework.demoqa_with_env import DemoQaWithEnv
from utils.base_session import BaseSession

load_dotenv()

LOGIN = "qa_guru_3_14@gu.ru"
PASSWORD = "123456"
API_URL = os.getenv('API_URL')
print(f"API_URL={API_URL}")
WEB_URL = os.getenv("WEB_URL")
print(f"WEB_URL={WEB_URL}")

browser.config.base_url = WEB_URL


def test_login():
    """Successful authorization to some demowebshop (UI)"""
    with step("Open login page"):
        browser.open("/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_though_api():
    response = requests.post(f"{API_URL}/login", json={"Email": "qa_guru_3_14@gu.ru", "Password": "123456"}, allow_redirects=False)
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    browser.open("/Themes/DefaultClean/Content/images/logo.png")

    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    browser.open("")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_though_api_with_base_session():
    demoshop = BaseSession(API_URL)
    response = demoshop.post("/login", json={"Email": "qa_guru_3_14@gu.ru", "Password": "123456"}, allow_redirects=False)
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    browser.open("/Themes/DefaultClean/Content/images/logo.png")

    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    browser.open("")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_though_api_with_base_session_fixture(demoshop):
    response = demoshop.post("/login", json={"Email": "qa_guru_3_14@gu.ru", "Password": "123456"}, allow_redirects=False)
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    browser.open("/Themes/DefaultClean/Content/images/logo.png")

    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    browser.open("")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_add_one_product_to_cart_authorized(demoshop):
    """Тест с прокидыванием сессии во фреймворк"""
    with step("Авторизоваться"):
        demoqa = DemoQA(demoshop)
        demoqa.authorization_cookie = demoqa.login(email=LOGIN, password=PASSWORD)

    with step("Добавление товара в корзину"):
        result = demoqa.add_to_cart(cookies=demoqa.authorization_cookie)

    with step("Товар добавлен в корзину"):
        assert result.status_code == 200
        assert 'The product has been added to your' in result.json()["message"]


def test_add_one_product_to_cart_authorized_with_env(env):
    """Тест с прокидыванием окружения во фреймворк"""
    with step("Авторизоваться"):
        demoqa = DemoQaWithEnv(env)
        demoqa.authorization_cookie = demoqa.login(email=LOGIN, password=PASSWORD)

    with step("Добавление товара в корзину"):
        result = demoqa.add_to_cart(cookies=demoqa.authorization_cookie)

    with step("Товар добавлен в корзину"):
        assert result.status_code == 200
        assert 'The product has been added to your' in result.json()["message"]
