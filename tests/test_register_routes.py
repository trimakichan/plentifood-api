from app.models.admin_user import AdminUser
from app.models.organization import Organization
from app.db import db
import pytest

def test_creates_both_records_links_them(client, valid_register_payload):
    # Arrange
    response = client.post("/register", json=valid_register_payload)
    response_body = response.get_json()
    
    # Assert: response basics
    assert response.status_code == 201
    assert "organization" in response_body
    assert "admin_user" in response_body

    org_json = response_body["organization"]
    admin_json = response_body["admin_user"]

    assert org_json["id"] is not None
    assert admin_json["id"] is not None
    assert admin_json["organization_id"] == org_json["id"]

    # Assert: DB side effects 
    org = db.session.get(Organization, org_json["id"])
    admin = db.session.get(AdminUser, admin_json["id"])

    assert org is not None
    assert admin is not None
    assert admin.organization_id == org.id
    assert org.website_url == valid_register_payload["organization"]["website"]
    assert admin.username == valid_register_payload["admin"]["username"]

def test_missing_key_admin(client, payload_missing_admin):
    # Arrange/Act
    response = client.post("/register", json=payload_missing_admin)
    response_body = response.get_json()

    # Assert: HTTP response
    assert response.status_code == 400
    assert response_body["message"] == "Invalid request: missing admin" 

    # Assert: DB side effects (no new records)
    assert db.session.query(AdminUser).count() == 0
    assert db.session.query(Organization).count() == 0


def test_missing_key_organization(client, payload_missing_organization):
    # Arrange/Act
    response = client.post("/register", json=payload_missing_organization)
    response_body = response.get_json()

    # Assert: HTTP response
    assert response.status_code == 400
    assert response_body["message"] == "Invalid request: missing organization" 

    # Assert: DB side effects (no new records)
    assert db.session.query(AdminUser).count() == 0
    assert db.session.query(Organization).count() == 0

# not sure if invalid-org-type path actually reaches that abort
def test_invalid_org_type(client, payload_invalid_org_type):
    # Arrange/Act
    response = client.post("/register", json=payload_invalid_org_type)
    response_body = response.get_json()

    # Assert: HTTP response
    assert response.status_code == 400
    assert response_body["details"] == "Invalid data"

    # Assert: DB side effects (no new records)
    assert db.session.query(AdminUser).count() == 0
    assert db.session.query(Organization).count() == 0


def test_website_url_mapping_validation(client, valid_register_payload):
    response = client.post("/register", json=valid_register_payload)
    response_body = response.get_json()
    
    assert response.status_code == 201

    org_json = response_body["organization"]
    assert org_json["website_url"] == valid_register_payload["organization"]["website_url"]

    # Assert: DB side effects 
    org = db.session.get(Organization, org_json["id"])
    assert org is not None
    assert org.website_url == valid_register_payload["organization"]["website_url"]
    

# do we need this?
def test_only_one_admin_is_constraint():
    pass
