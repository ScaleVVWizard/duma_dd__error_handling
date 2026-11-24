import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_custom_exception_a():
    response = client.get("/test/a/-5")
    assert response.status_code == 409
    data = response.json()
    assert data["error_type"] == "CustomAError"
    assert data["status_code"] == 409

def test_custom_exception_b():
    response = client.get("/test/b/200")
    assert response.status_code == 404
    data = response.json()
    assert data["error_type"] == "CustomError"
    assert data["status_code"] == 404

def test_validation_error():
    payload = {
        "username": "a",
        "age": 17,
        "email": "not-email",
        "password": "short"
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == 422
    assert data["title"] == "Validation Error"
    assert len(data["errors"]) > 0

def test_http_exception():
    response = client.get("/test/http-error")
    assert response.status_code == 403
    data = response.json()
    assert data["error_type"] == "HTTPException"

def test_unexpected_exception():
    with TestClient(app, raise_server_exceptions=False) as c:
        response = c.get("/test/boom")
        assert response.status_code == 500
        data = response.json()
        assert data["error_type"] == "InternalServerError"