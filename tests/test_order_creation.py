import allure
import requests
from helpers import create_order, get_ingredients
from data import INVALID_HASH
from urls import ORDERS_ENDPOINT

@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, registered_user):
        token = registered_user["token"]
        ingredient_ids = [get_ingredients()[0]["_id"], get_ingredients()[1]["_id"]]
        resp = create_order(token, ingredient_ids)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "order" in data

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredient_ids = [get_ingredients()[0]["_id"], get_ingredients()[1]["_id"]]
        resp = requests.post(ORDERS_ENDPOINT, json={"ingredients": ingredient_ids})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "order" in data

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        resp = requests.post(ORDERS_ENDPOINT, json={"ingredients": []})
        assert resp.status_code == 400
        assert resp.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_hash(self):
        resp = requests.post(ORDERS_ENDPOINT, json={"ingredients": [INVALID_HASH]})
        assert resp.status_code == 500