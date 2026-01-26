from app.models.admin_user import AdminUser
from datetime import datetime, timezone
from app.db import db


def test_login_returns_200_and_admin_info(client, saved_admin_user):
    # Act
    response = client.post("/login", json={"username": "test_admin"})
    data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert data["id"] == saved_admin_user.id
    assert data["username"] == "test_admin"


def test_login_returns_404_when_username_not_found(client):
    # Act
    response = client.post("/login", json={"username": "wrong_admin"})
    data = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "error" in data
    assert data["error"] == "Admin not found"


def test_login_returns_400_when_username_missing(client):
    # Act
    response = client.post("/login", json={})
    data = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "error" in data

def test_get_me_returns_200_when_valid_header(client, saved_admin_user):
    # Act
    response = client.get(
        "/login/me",
        headers={"X-User-Id": str(saved_admin_user.id)}
    )
    data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert data["id"] == saved_admin_user.id
    assert data["username"] == "test_admin"
    assert data["organization_id"] == saved_admin_user.organization_id


def test_get_me_returns_401_when_missing_header(client):
    # Act
    response = client.get("/login/me")
    data = response.get_json()

    # Assert
    assert response.status_code == 401
    assert "error" in data