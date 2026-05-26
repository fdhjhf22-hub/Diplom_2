import random
import string
import requests
import allure
from urls import REGISTER_ENDPOINT, LOGIN_ENDPOINT, INGREDIENTS_ENDPOINT, DELETE_USER_ENDPOINT, ORDERS_ENDPOINT

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def register_user(email, password, name):
    with allure.step(f"Регистрируем пользователя {email}"):
        resp = requests.post(REGISTER_ENDPOINT, json={
            "email": email, "password": password, "name": name
        })
    return resp

def login_user(email, password):
    with allure.step(f"Логинимся как {email}"):
        resp = requests.post(LOGIN_ENDPOINT, json={
            "email": email, "password": password
        })
    return resp

def get_ingredients():
    with allure.step("Получаем список ингредиентов"):
        resp = requests.get(INGREDIENTS_ENDPOINT)
        resp.raise_for_status()
    return resp.json()["data"]

def create_order(token, ingredient_ids):
    headers = {"Authorization": token}
    with allure.step("Создаём заказ"):
        resp = requests.post(ORDERS_ENDPOINT, headers=headers, json={
            "ingredients": ingredient_ids
        })
    return resp

def delete_user(token):
    with allure.step("Удаляем пользователя"):
        headers = {"Authorization": token}
        resp = requests.delete(DELETE_USER_ENDPOINT, headers=headers)
    return resp