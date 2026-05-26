import allure
import requests
from helpers import login_user
from data import DEFAULT_PASSWORD
from urls import LOGIN_ENDPOINT

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_success(self, registered_user):
        email = registered_user["email"]
        resp = login_user(email, DEFAULT_PASSWORD)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "accessToken" in data

    @allure.title("Вход с неверным логином и паролем")
    def test_login_wrong_credentials(self):
        resp = requests.post(LOGIN_ENDPOINT, json={
            "email": "nonexistent@ya.ru",
            "password": "wrong"
        })
        assert resp.status_code == 401
        assert resp.json()["message"] == "email or password are incorrect"