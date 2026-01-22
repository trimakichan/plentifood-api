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
    assert org.website_url == valid_register_payload["organization"]["website_url"]
    assert admin.username == valid_register_payload["admin"]["username"]

