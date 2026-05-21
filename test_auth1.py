import pytest


def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"username": "newuser", "email": "new@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_register_duplicate_username(client, registered_user):
    response = client.post(
        "/auth/register",
        json={"username": registered_user["username"], "email": "other@example.com", "password": "pass"},
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_register_duplicate_email(client, registered_user):
    response = client.post(
        "/auth/register",
        json={"username": "differentuser", "email": registered_user["email"], "password": "pass"},
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client, registered_user):
    response = client.post(
        "/auth/login",
        json={"username": registered_user["username"], "password": registered_user["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    response = client.post(
        "/auth/login",
        json={"username": registered_user["username"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        json={"username": "nobody", "password": "password"},
    )
    assert response.status_code == 401
