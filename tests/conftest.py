from datetime import datetime, timezone
import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.db import db
from app.models.site import Eligibility, Site, SiteStatus
from app.models.service import Service
from app.models.organization import Organization, OrgType
from app.models.admin_user import AdminUser


load_dotenv()


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get("SQLALCHEMY_DATABASE_URI_TEST"),
    }

    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_organization(app):
    """Create and save a test organization."""
    org = Organization(
        name="Test Organization",
        organization_type=OrgType.FOOD_TYPE,
        website_url="https://test.org",
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(org)
    db.session.commit()
    return org


@pytest.fixture
def valid_site_dict(test_organization):
    return {
        "name": "Algona/Pacific Food Pantry - Food Distribution Center",
        "address_line1": "603 3rd Ave SE",
        "city": "Algona",
        "state": "WA",
        "postal_code": "98001",
        "latitude": 47.265011,
        "longitude": -122.236,
        "phone": "123-456-7890",
        "eligibility": "olderAdultsAndEligible",
        "hours": {
            "sunday": [{"open": "10:00", "close": "14:00"}],
            "monday": [{"open": "10:00", "close": "14:00"}],
            "tuesday": [{"open": "10:00", "close": "14:00"}],
            "wednesday": [],
            "thursday": [{"open": "12:00", "close": "16:00"}],
            "friday": [{"open": "10:00", "close": "13:00"}],
            "saturday": [],
        },
        "service_notes": "No special notes",
        "organization_id": test_organization.id,
        "services": ["food_bank"]
    }


@pytest.fixture
def one_saved_site(app, test_organization):
    site = Site(
        name="Test Site",
        status=SiteStatus.OPEN,
        address_line1="603 3rd Ave SE",
        address_line2=None,
        city="Algona",
        state="WA",
        postal_code="98001",
        latitude=47.265011,
        longitude=-122.236,
        phone="123-456-7890",
        eligibility=Eligibility.OLDER_ADULTS_AND_ELIGIBLE,
        hours={
            "sunday": [{"open": "10:00", "close": "14:00"}],
            "monday": [{"open": "10:00", "close": "14:00"}],
            "tuesday": [{"open": "10:00", "close": "14:00"}],
            "wednesday": [],
            "thursday": [{"open": "12:00", "close": "16:00"}],
            "friday": [{"open": "10:00", "close": "13:00"}],
            "saturday": [],
        },
        service_notes="No notes",
        organization_id=test_organization.id,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    db.session.add(site)
    db.session.commit()
    return site

@pytest.fixture
def two_saved_sites(app, test_organization):
    site_a = Site(
        name="Test Site",
        status=SiteStatus.OPEN,
        address_line1="603 3rd Ave SE",
        address_line2=None,
        city="Algona",
        state="WA",
        postal_code="98001",
        latitude=47.265011,
        longitude=-122.236,
        phone="123-456-7890",
        eligibility=Eligibility.OLDER_ADULTS_AND_ELIGIBLE,
        hours={
            "sunday": [],
            "monday": [],
            "tuesday": [],
            "wednesday": [{"open": "10:00", "close": "13:00"}],
            "thursday": [{"open": "12:00", "close": "16:00"}],
            "friday": [],
            "saturday": [],
    },
        service_notes="No notes",
        organization_id=test_organization.id,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    

    site_b = Site(
        name="Auburn Food Bank",
        status=SiteStatus.OPEN,
        address_line1="100 N St SE",
        address_line2=None,
        city="Auburn",
        state="WA",
        postal_code="98002",
        latitude=47.3327,
        longitude=-122.22159,
        phone="(253)-833-8925",
        eligibility=Eligibility.GENERAL_PUBLIC,
        hours={
            "sunday": [],
            "monday": [{"open": "10:00", "close": "14:00"}],
            "tuesday": [{"open": "10:00", "close": "14:00"}],
            "wednesday": [],
            "thursday": [{"open": "10:00", "close": "14:00"}],
            "friday": [{"open": "10:00", "close": "14:00"}],
            "saturday": [],
        },
        service_notes=(
            "Serves residents of Auburn School District; "
            "Not required to show proof of residence for the food program. "
            "Curbside/car drop off for existing clients; "
            "if new client, application will need to be filled out quickly inside. "
            "On the 2nd Wednesday of the Month, we provide Evening Food Bank services "
            "from 5:30pm to 6:15pm."
        ),
        organization_id=test_organization.id,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    db.session.add_all([site_a, site_b])
    db.session.commit()


@pytest.fixture
def three_saved_sites(app, test_organization):
    site_wed = Site(
        name="Wed Site",
        status=SiteStatus.OPEN,
        address_line1="1 A St",
        address_line2=None,
        city="Algona",
        state="WA",
        postal_code="98001",
        latitude=47.26,
        longitude=-122.23,
        phone="111",
        eligibility=Eligibility.GENERAL_PUBLIC,
        hours={
            "sunday": [],
            "monday": [],
            "tuesday": [],
            "wednesday": [{"open": "10:00", "close": "14:00"}],
            "thursday": [],
            "friday": [],
            "saturday": [],
        },
        service_notes="",
        organization_id=test_organization.id,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    site_fri = Site(
        name="Fri Site",
        status=SiteStatus.OPEN,
        address_line1="2 B St",
        address_line2=None,
        city="Auburn",
        state="WA",
        postal_code="98002",
        latitude=47.33,
        longitude=-122.22,
        phone="222",
        eligibility=Eligibility.GENERAL_PUBLIC,
        hours={
            "sunday": [],
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [{"open": "10:00", "close": "14:00"}],
            "saturday": [],
        },
        service_notes="",
        organization_id=test_organization.id,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    site_mon = Site(
        name="Mon Site",
        status=SiteStatus.OPEN,
        address_line1="3 C St",
        address_line2=None,
        city="Seattle",
        state="WA",
        postal_code="98144",
        latitude=47.57,
        longitude=-122.29,
        phone="333",
        eligibility=Eligibility.GENERAL_PUBLIC,
        hours={
            "sunday": [],
            "monday": [{"open": "10:00", "close": "14:00"}],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
        },
        service_notes="",
        organization_id=test_organization.id,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    db.session.add_all([site_wed, site_fri, site_mon])
    db.session.commit()

    return site_wed, site_fri, site_mon

####################################
# Service #
####################################
@pytest.fixture
def valid_service_dict():
    return {
        "name": "food_bank"
    }

@pytest.fixture
def valid_service():
    return Service(
        name="food_bank"
    )

@pytest.fixture
def two_saved_services(app):
    # Arrange
    service_one = Service(name="food_bank")
    service_two = Service(name="meal")

    db.session.add_all([service_one, service_two])
    db.session.commit()


####################################
# Admin, Organization and register #
####################################

@pytest.fixture
def valid_admin_dict():
    return {
        "username": "test_user",
    }


@pytest.fixture
def valid_admin_user():
    return AdminUser(
        username="Test User",
        created_at=datetime.now(timezone.utc),
    )

@pytest.fixture
def valid_organization_dict():
    return {
        "name": "Test Organization",
        "organization_type": "non_profit",
        "website_url": "https://example.com"
    }

@pytest.fixture
def valid_organization():
    return Organization(
        name="Test Organization",
        organization_type=OrgType("non_profit"),
        website_url="https://example.com",
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

# register_routes
@pytest.fixture
def valid_register_payload():
    return {
    "organization": {
        "name": "Asian Counseling and Referral Service",
        "organization_type": "church",
        "website_url": "https://acrs.org/services/aging-services-for-older-adults/acrs-food-bank/"
    },
    "admin": {
        "username": "Test register"
    }
    }

@pytest.fixture
def payload_missing_admin():
    return {
        "organization": {
            "name": "Asian Counseling and Referral Service",
            "organization_type": "church",
            "website_url": "https://acrs.org/services/aging-services-for-older-adults/acrs-food-bank/"
        },
    }

@pytest.fixture
def payload_missing_organization():
    return {
        "admin": {
            "username": "Test register"
        }
    }

@pytest.fixture
def payload_invalid_org_type():
    return {
        "organization": {
            "name": "Asian Counseling and Referral Service",
            "organization_type": "restaurant",
            "website_url": "https://acrs.org/services/aging-services-for-older-adults/acrs-food-bank/"
    },
        "admin": {
            "username": "Test register"
    }
    }

