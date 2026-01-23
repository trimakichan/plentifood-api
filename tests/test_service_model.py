from app.models.service import Service
from app.db import db
import copy
import pytest

def test_from_dict_returns_service(valid_service_dict):
    # Act
    service = Service.from_dict(valid_service_dict)

    # Assert
    assert service.name == valid_service_dict["name"]
    assert service.id is None

def test_from_dict_missing_name(valid_service_dict):
    # Arrange
    service_dict = valid_service_dict.copy()
    service_dict.pop("name")

    # Act and Assert
    with pytest.raises(KeyError, match="name"):
        service = Service.from_dict(service_dict)

def test_from_dict_with_extra_keys(valid_service_dict):
    # Arrange
    service_dict = valid_service_dict.copy()
    service_dict["extra"] = "extra stuff"

    # Act
    service = Service.from_dict(service_dict)

    # Assert
    assert service.id is None
    assert service.name == service_dict["name"]

def test_to_dict_returns_correct_dict(valid_service):
    # Act
    service_dict = valid_service.to_dict()

    # Assert
    assert service_dict["id"] is None
    assert service_dict["name"] == valid_service.name

def test_to_dict_missing_name():
    # Arrange
    service = Service(id=1)

    # Act
    service_dict = service.to_dict()

    # Assert
    assert len(service_dict) == 2
    assert service_dict["id"] == 1
    assert service_dict["name"] is None

