import pytest
from helpers import register_user, delete_user, generate_random_string
from data import DEFAULT_PASSWORD, DEFAULT_USER_NAME

@pytest.fixture(scope="function")
def registered_user():
    """Фикстура создаёт уникального пользователя и возвращает его данные + ответ сервера.
    После теста пользователь удаляется."""
    email = f"test_{generate_random_string()}@ya.ru"
    password = DEFAULT_PASSWORD
    name = DEFAULT_USER_NAME

    # Создаём пользователя (без assert, чтобы не тестировать в фикстуре)
    resp = register_user(email, password, name)

    yield {
        "email": email,
        "password": password,
        "name": name,
        "token": resp.json().get("accessToken"),
        "response": resp
    }

    # Удаляем пользователя после теста
    token = resp.json().get("accessToken")
    if token:
        delete_user(token)