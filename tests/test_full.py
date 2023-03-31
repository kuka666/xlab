import json
import pytest
from fastapi.testclient import TestClient

from ..src.app import app


client = TestClient(app)


@pytest.fixture
def example_user():
    return {
        "name": "Аман",
        "surname": "Аманов",
        "patronymic": "Аманович",
        "phone_number": "79998887766",
        "email": "ivanov@example.com",
        "country": "Россия"
    }


def test_create_user(example_user: dict[str, str]):
    response = client.post("/save_user_data", json=example_user)
    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "date_created" in response.json()


def test_get_user_data(example_user: dict[str, str]):
    # сначала создаем пользователя
    response = client.post("/save_user_data", json=example_user)
    assert response.status_code == 200

    # затем получаем его данные
    response = client.get(
        f"/get_user_data?phone_number={example_user['phone_number']}")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["name"] == example_user["name"]
    assert user_data["surname"] == example_user["surname"]
    assert user_data["patronymic"] == example_user["patronymic"]
    assert user_data["phone_number"] == example_user["phone_number"]
    assert user_data["email"] == example_user["email"]
    assert user_data["country"] == example_user["country"]


def test_delete_user_data(example_user: dict[str, str]):
    # сначала создаем пользователя
    response = client.post("/save_user_data", json=example_user)
    assert response.status_code == 200

    # затем удаляем его данные
    response = client.delete(
        f"/delete_user_data?phone_number={example_user['phone_number']}")
    assert response.status_code == 200

    # пытаемся получить данные пользователя, должны получить ошибку 404
    response = client.get(
        f"/get_user_data?phone_number={example_user['phone_number']}")
    assert response.status_code == 404
