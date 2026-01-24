from app.models.admin_user import AdminUser
from app.models.organization import Organization, OrgType
from app.db import db
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
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
    assert response_body == {"details": "Invalid data: 'restaurant'"}

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
    

# check admin_user has unique org_id
def test_admin_user_organization_id_must_be_unique(app):
    # Create org and commit
    org = Organization(
        name="Uniq Org",
        organization_type=OrgType.from_frontend("nonProfit"),
        website_url="https://example.com",
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )
    db.session.add(org)
    db.session.commit()

    # Create admin1 linked to org and commit
    admin1 = AdminUser(
        username="admin1",
        organization_id=org.id,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(admin1)
    db.session.commit()

    # Create admin2 linked to the SAME org (should violate unique constraint)
    admin2 = AdminUser(
        username="admin2",
        organization_id=org.id,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(admin2)

    with pytest.raises(IntegrityError):
        db.session.commit()

    # After IntegrityError, session must be rolled back before any more DB work
    db.session.rollback()

    # Assert only one AdminUser row exists for that org id
    admins_for_org = db.session.query(AdminUser).filter_by(organization_id=org.id).all()
    assert len(admins_for_org) == 1
    assert admins_for_org[0].username == "admin1"
