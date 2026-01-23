from datetime import datetime, timezone
from app.models.admin_user import AdminUser
from app.db import db
import pytest
import copy


def test_from_dict_returns_admin(valid_admin_dict):
    # Act
    admin = AdminUser.from_dict(valid_admin_dict)
    #Asset
    assert admin.username == valid_admin_dict["username"]
    assert admin.created_at is not None


def test_from_dict_missing_username(valid_admin_dict):
    # Arrange
    admin_dict = valid_admin_dict.copy()
    admin_dict.pop("username")

    # Act and Assert
    with pytest.raises(KeyError, match="username"):
        admin = AdminUser.from_dict(admin_dict)

def test_from_dict_with_extra_keys(valid_admin_dict):
    # Arrange
    admin_dict = valid_admin_dict.copy()
    admin_dict["extra"] = "extra stuff"

    # Act
    admin = AdminUser.from_dict(admin_dict)

    # Assert
    assert admin.id is None
    assert admin.username == admin_dict["username"]
    

def test_to_dict_returns_correct_dict(valid_admin_user):
    # Act
    admin_dict = valid_admin_user.to_dict()

    # Assert
    assert len(admin_dict) == 4
    assert admin_dict["id"] is None
    assert admin_dict["username"] == valid_admin_user.username
    assert isinstance(admin_dict["created_at"], str)

def test_to_dict_missing_username():
    # Arrange
    admin_user = AdminUser(
        id=1,
        created_at=datetime.now(timezone.utc),
        )

    # Act
    admin_dict = admin_user.to_dict()

    # Assert
    assert len(admin_dict) == 4
    assert admin_dict["id"] == 1
    assert admin_dict["username"] is None
    assert isinstance(admin_dict["created_at"], str)
