from app.models.admin_user import AdminUser
from app.db import db
import pytest
import copy


def test_from_dict_returns_admin(valid_admin_dict):
    # Arrange

    # Act
    admin = AdminUser.from_dict(valid_admin_dict)
    #Asset
    assert admin.username == valid_admin_dict["username"]
    assert admin.created_at is not None


def test_from_dict_missing_username(valid_admin_dict):
    # Arrange
    admin_dict = copy.deepcopy(valid_admin_dict)
    admin_dict.pop("username")

    # Act and Assert
    with pytest.raises(KeyError, match="username"):
        admin = AdminUser.from_dict(admin_dict)

def test_to_dict_returns_correct_dict(valid_admin_user):
    # Arrange
    # Act
    admin_dict = valid_admin_user.to_dict()

    # Assert
    assert admin_dict["id"] is None
    assert admin_dict["username"] == valid_admin_user.username
    assert isinstance(admin_dict["created_at"], str)

def test_to_dict_missing_id(valid_admin_user):
    # Act
    admin_dict = valid_admin_user.to_dict()

    # Assert
    assert admin_dict['id'] is None