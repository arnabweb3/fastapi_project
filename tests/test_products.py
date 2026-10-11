from main import app
from fastapi.testclient import TestClient



client = TestClient(app)

def test_get_products():

    response = client.get("/products/")

    assert response.status_code == 200

    assert isinstance(response.json() , list)

def test_create_product():
    payload = {
        "name": "Pytest Product",
        "price": 100.0,
        "quantity": 5,
        "description": "Created during automated testing"
    }

    response = client.post("/products/", json=payload)
    print(response.json())  # Add this line

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["quantity"] == payload["quantity"]
    assert data["id"] is not None


def test_create_product_with_negative_price():
    payload = {
        "name": "Invalid Product",
        "price": -10,
        "quantity": 5
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 422


def test_get_product_by_id():
    payload = {
        "name": "Retrieval Test",
        "price": 50,
        "quantity": 3,
    }
    created = client.post("/products/", json=payload)
    product_id = created.json()["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["id"] == product_id


def test_update_product():
    payload = {
        "name": "Update Test",
        "price": 50,
        "quantity": 3,
    }
    created = client.post("/products/", json=payload)
    product_id = created.json()["id"]

    response = client.patch(
        f"/products/{product_id}",
        json={"quantity": 10},
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 10
    assert response.json()["name"] == "Update Test"


def test_delete_product():
    payload = {
        "name": "Delete Test",
        "price": 25,
        "quantity": 1,
    }
    created = client.post("/products/", json=payload)
    product_id = created.json()["id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 204

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404