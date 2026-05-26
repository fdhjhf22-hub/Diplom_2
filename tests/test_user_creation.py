import allure
import pytest
from helpers import register_user, generate_random_string
from data import DEFAULT_PASSWORD, DEFAULT_USER_NAME
from urls import REGISTER_ENDPOINT
import requests

@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешная регистрация нового пользователя")
    def test_unique_user_success(self, registered_user):
        resp = registered_user["response"]
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "accessToken" in data

    @allure.title("Регистрация уже существующего пользователя")
    def test_existing_user_forbidden(self, registered_user):
        email = registered_user["email"]
        resp = register_user(email, DEFAULT_PASSWORD, DEFAULT_USER_NAME)
        assert resp.status_code == 403
        assert resp.json()["message"] == "User already exists"

    @allure.title("Регистрация без обязательного поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_missing_required_field(self, field):
        email = f"test_{generate_random_string()}@ya.ru"
        payload = {"email": email, "password": DEFAULT_PASSWORD, "name": DEFAULT_USER_NAME}
        del payload[field]
        resp = requests.post(REGISTER_ENDPOINT, json=payload)
        assert resp.status_code == 403
        assert resp.json()["message"] == "Email, password and name are required fields"