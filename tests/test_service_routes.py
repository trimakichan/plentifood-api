from werkzeug.exceptions import HTTPException
from app.db import db
import pytest

# --------------create_service--------------

def test_create_one_service(client):
    # Act
    response = client.post("/services", json={
        "name": "food_bank"
    })
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 201
    assert isinstance(response_body["id"], int)
    assert response_body["name"] == "food_bank"

def test_create_one_service_no_name(client):
    # Arrange
    service_dict = {}

    # Act
    response = client.post("/services", json=service_dict)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data: 'name'"}

def test_create_one_service_with_extra_keys(client, valid_service_dict):
    # Arrange
    service_dict = valid_service_dict.copy()
    service_dict["extra"] = "extra stuff"

    # Act
    response = client.post("/services", json=service_dict)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "food_bank"
    }
    

def test_get_all_services_one_saved_service(client, two_saved_services):
    # Act
    response = client.get("/services")
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "name": "food_bank"
    }

def test_get_all_services_no_saved_service(client):
    # Act
    response = client.get("/services")
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200
    assert len(response_body) == 0
    assert response_body == []

