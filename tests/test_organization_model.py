from app.models.admin_user import AdminUser
from app.models.organization import Organization, OrgType
from app.db import db
import pytest
import copy


def test_from_dict_returns_organization(valid_organization_dict):
    # Arrange

    # Act
    organization = Organization.from_dict(valid_organization_dict)
    #Asset
    assert organization.name == valid_organization_dict["name"]
    assert organization.organization_type == OrgType.NON_PROFIT.value
    assert organization.created_at is not None


def test_from_dict_missing_name(valid_organization_dict):
    # Arrange
    valid_organization_dict = copy.deepcopy(valid_organization_dict)
    valid_organization_dict.pop("name")

    # Act and Assert
    with pytest.raises(KeyError, match="name"):
        organization = Organization.from_dict(valid_organization_dict)

def test_to_dict_returns_correct_dict(valid_organization):
    # Arrange
    # Act
    org_dict = valid_organization.to_dict()

    # Assert
    assert org_dict["id"] is None
    assert org_dict["name"] == valid_organization.name
    assert isinstance(org_dict["created_at"], str)
    assert org_dict["updated_at"] is None

def test_to_dict_missing_items(valid_organization):
    # Act
    org_dict = valid_organization.to_dict()

    # Assert
    assert org_dict["id"] is None
    assert org_dict["name"] == valid_organization.name
    assert org_dict["organization_type"] == valid_organization.organization_type
    assert org_dict["website_url"] == valid_organization.website_url
    assert isinstance(org_dict["created_at"], str)
