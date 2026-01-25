from app.models.admin_user import AdminUser
from app.models.organization import Organization, OrgType
from app.models.site import Site
from app.models.service import Service
from app.db import db
from datetime import datetime, timezone
import pytest

## create_site ##
def test_create_site_returns_201_with_latlon(client, organization_id, valid_site_dict_no_param):
    for name in valid_site_dict_no_param["services"]:
        db.session.add(Service(name=name))
    db.session.commit()

    # Act
    response = client.post(f"/organizations/{organization_id}/sites", json=valid_site_dict_no_param)
    assert response.status_code == 201, response.get_json()

    data = response.get_json()
    
    assert "id" in data

    # Assert DB truth (don’t depend on response containing organization_id)
    site = db.session.get(Site, data["id"])
    assert site is not None
    assert site.organization_id == organization_id


def test_create_site_without_latlon(client, organization_id, valid_site_dict_no_param, monkeypatch):

    for name in valid_site_dict_no_param["services"]:
        db.session.add(Service(name=name))
    db.session.commit()

    # Remove lat/lon from payload
    payload = dict(valid_site_dict_no_param)  # shallow copy
    payload.pop("latitude", None)
    payload.pop("longitude", None)

    # Mock get_coordinates (patch where it's imported/used: the route module)
    def fake_get_coordinates(request_body):
        return {"latitude": 1.23, "longitude": 4.56}
    
    monkeypatch.setattr("app.routes.organization_routes.get_coordinates", fake_get_coordinates)

    # Act
    response = client.post(f"/organizations/{organization_id}/sites", json=payload)

    # Assert
    assert response.status_code == 201, response.get_json()
    data = response.get_json()
    assert "id" in data

    site = db.session.get(Site, data["id"])
    assert site is not None
    assert site.organization_id == organization_id
    assert site.latitude == 1.23
    assert site.longitude == 4.56


def test_create_site_services_contains_invalid_name(client, organization_id, valid_site_dict_no_param):
    # Arrange: create only ONE valid service in DB
    db.session.add(Service(name="food_bank"))
    db.session.commit()

    payload = dict(valid_site_dict_no_param)
    payload["services"] = ["food_bank", "not_a_real_service"]

    # Act
    response = client.post(f"/organizations/{organization_id}/sites", json=payload)

    # Assert
    assert response.status_code == 400
    data = response.get_json()
    assert data == {"details": "One or more services are invalid."}


def test_create_site_missing_required_key(client, organization_id, valid_site_dict_no_param):
    # Arrange: create required services in DB
    for name in valid_site_dict_no_param["services"]:
        db.session.add(Service(name=name))
    db.session.commit()

    payload = dict(valid_site_dict_no_param)
    payload.pop("hours")  # remove required field

    # Act
    response = client.post(f"/organizations/{organization_id}/sites", json=payload)

    # Assert
    assert response.status_code == 400
    data = response.get_json()
    assert data["details"] == "Invalid data: 'hours'"    


def test_create_site_get_coordinates_raises_value_error(client, organization_id, valid_site_dict_no_param, monkeypatch):
    
    # Arrange: create required services in DB
    for name in valid_site_dict_no_param["services"]:
        db.session.add(Service(name=name))
    db.session.commit()

    # Remove latitude and longitude so get_coordinates is called
    payload = dict(valid_site_dict_no_param)
    payload.pop("latitude", None)
    payload.pop("longitude", None)

    # Fake get_coordinates that raises ValueError
    def fake_get_coordinates(request_body):
        raise ValueError("LocationIQ service is unavailable")

    # Patch the function where it is used (adjust module path if needed)
    monkeypatch.setattr(
        "app.routes.organization_routes.get_coordinates",
        fake_get_coordinates
    )

    # Act
    response = client.post(f"/organizations/{organization_id}/sites", json=payload)

    # Assert
    assert response.status_code == 502
    data = response.get_json()
    assert data["details"] == "LocationIQ service is unavailable"


## get_organiztaion ##
def test_get_organization_returns_200_org_dict_found(client, organization_id):
    response = client.get(f"/organizations/{organization_id}")
    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == organization_id
    assert data["name"] == "Test Organization"
    assert data["organization_type"] == "food_bank"  # matches OrgType.FOOD_BANK.value
    assert data["website_url"] == "https://test.org"


## get_organization_sites ## 
def test_get_organization_sites_returns_200_only_that_org(client, organization_id, valid_site_dict_no_param):
    # Arrange
    # Create the service used in payload
    for name in valid_site_dict_no_param["services"]:
        db.session.add(Service(name=name))
    db.session.commit()

    # Create a second organization
    other_org = Organization(
        name="Other Organization",
        organization_type=OrgType.CHURCH,
        website_url="https://other.org",
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(other_org)
    db.session.commit()

    # Create a site for the main organization
    site_for_org = Site.from_dict(valid_site_dict_no_param, org_id=organization_id)
    site_for_org.organization_id = organization_id
    db.session.add(site_for_org)

    # Create a site for the other organization
    site_for_other_org = Site.from_dict(valid_site_dict_no_param, org_id=other_org.id)
    site_for_other_org.organization_id = other_org.id
    db.session.add(site_for_other_org)

    db.session.commit()

    # Act
    response = client.get(f"/organizations/{organization_id}/sites")

    # Assert
    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 1  # only one site should belong to this org
    assert data[0]["id"] == site_for_org.id


def test_get_organization_returns_400_org_not_found(client):
    # Pick an ID that definitely does not exist
    nonexistent_org_id = 999999

    # Act
    response = client.get(f"/organizations/{nonexistent_org_id}")

    # Assert
    assert response.status_code == 404

    data = response.get_json()
    assert data == {"message": f"Organization {nonexistent_org_id} not found"}


## update_organization ##
def test_update_organization_allowed_field_only(client, organization_id):
    # Arrange: load org from DB to capture original values
    org_before = db.session.get(Organization, organization_id)
    original_created_at = org_before.created_at
    original_id = org_before.id

    payload = {
        "name": "Updated Org Name",             # allowed
        "created_at": "2000-01-01T00:00:00Z",   # NOT allowed (should be ignored)
        "id": 9999,                             # NOT allowed (should be ignored)
    }

    # Act
    response = client.patch(f"/organizations/{organization_id}", json=payload)

    # Assert
    assert response.status_code == 204

    # Refresh / reload from DB
    org_after = db.session.get(Organization, organization_id)

    assert org_after.name == "Updated Org Name"          # changed
    assert org_after.id == original_id                   # not changed
    assert org_after.created_at == original_created_at   # not changed
    assert org_after.updated_at is not None              # set by route


## delete_organization ##
def test_update_organization_when_request_body_empty(client, organization_id):
    # Act
    response = client.patch(f"/organizations/{organization_id}", json={})

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"message": "Request body cannot be empty."}
    
    
def test_delete_organization(client, organization_id):
    # Sanity check: org exists before delete
    org = db.session.get(Organization, organization_id)
    assert org is not None

    # Act
    response = client.delete(f"/organizations/{organization_id}")

    # Assert
    assert response.status_code == 204

    # Organization should be gone
    deleted_org = db.session.get(Organization, organization_id)
    assert deleted_org is None

