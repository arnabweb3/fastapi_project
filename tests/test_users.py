from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/users/register",
        json={
            "email": "register_test@example.com",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "register_test@example.com"
    assert "hashed_password" not in data
    assert "password" not in data
    assert isinstance(data["id"], int)


def test_register_duplicate_email():
    email = "duplicate_test@example.com"
    payload = {"email": email, "password": "StrongPass123"}

    first_response = client.post("/users/register", json=payload)
    second_response = client.post("/users/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_register_invalid_email():
    response = client.post(
        "/users/register",
        json={"email": "not-an-email", "password": "StrongPass123"},
    )

    assert response.status_code == 422


def test_register_short_password():
    response = client.post(
        "/users/register",
        json={"email": "short_password@example.com", "password": "short"},
    )

    assert response.status_code == 422