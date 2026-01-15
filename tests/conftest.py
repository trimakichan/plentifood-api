from datetime import datetime
import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.db import db
from app.models.site import Eligibility, Site, SiteStatus
from app.models.service import Service


load_dotenv()


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI_TEST": os.environ.get("SQLALCHEMY_DATABASE_URI_TEST"),
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


# This is for tests that make HTTP requests.
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def valid_site_dict():
    return {
        "name": "Algona/Pacific Food Pantry - Food Distribution Center",
        "status": "Open",
        "address_line1": "603 3rd Ave SE",
        "city": "Algona",
        "state": "WA",
        "postal_code": "98001",
        "latitude": 47.265011,
        "longitude": -122.236,
        "phone": "123-456-7890",
        "eligibility": "Older Adults 60+ and Eligible Participants",
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
    }


@pytest.fixture
def valid_site():
    return Site(
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
        hours={},
        service_notes="No notes",
        created_at=datetime.now(),
        updated_at=None,
    )


# Seeding services. check this later@pytest.fixture
# def seed_services(app):
#     # Create developer-controlled lookup values
#     services = [
#         Service(name="Food Bank"),
#         Service(name="Meal"),
#     ]

#     for s in services:
#         exists = Service.query.filter_by(name=s.name).first()
#         if not exists:
#             db.session.add(s)

#     db.session.commit()
#     return {s.name: Service.query.filter_by(name=s.name).first() for s in services}
