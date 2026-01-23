from app.models.site import Eligibility, Site, SiteStatus
from app.db import db
from datetime import datetime, timezone
import pytest
import copy


# --------------Helper functions--------------
def assert_site_matches_dict(site, dict_data):
    assert site.name == dict_data["name"]
    assert site.status == SiteStatus.OPEN
    assert isinstance(site.status, SiteStatus)
    assert site.address_line1 == dict_data["address_line1"]
    assert site.address_line2 == dict_data.get("address_line2")
    assert site.city == dict_data["city"]
    assert site.state == dict_data["state"]
    assert site.postal_code == dict_data["postal_code"]
    assert site.latitude == dict_data["latitude"]
    assert site.longitude == dict_data["longitude"]
    assert site.phone == dict_data["phone"]
    assert site.eligibility == Eligibility.OLDER_ADULTS_AND_ELIGIBLE
    assert isinstance(site.eligibility, Eligibility)
    assert site.hours == dict_data["hours"]
    assert site.service_notes == dict_data.get("service_notes", "")
    assert site.created_at is not None
    assert site.updated_at is None

def assert_dict_matches_site(site, dict_data):
    assert dict_data["id"] is site.id
    assert dict_data["name"] == site.name
    assert dict_data["status"] == SiteStatus.OPEN.value
    assert dict_data["address_line1"] == site.address_line1
    assert dict_data["address_line2"] is None
    assert dict_data["city"] == site.city
    assert dict_data["state"] == site.state
    assert dict_data["postal_code"] == site.postal_code
    assert dict_data["latitude"] == site.latitude
    assert dict_data["longitude"] == site.longitude
    assert dict_data["phone"] == site.phone
    assert dict_data["eligibility"] == Eligibility.OLDER_ADULTS_AND_ELIGIBLE.value
    assert dict_data["hours"] == site.hours
    assert dict_data["service_notes"] == site.service_notes
    assert isinstance(dict_data["created_at"], str)
    assert dict_data["updated_at"] is None


def test_from_dict_returns_site(valid_site_dict,test_organization):
    # Act
    site = Site.from_dict(valid_site_dict)
    # Assert
    assert_site_matches_dict(site, valid_site_dict)


def test_from_dict_missing_name(valid_site_dict):
    # Arrange
    site_dict = copy.deepcopy(valid_site_dict)
    site_dict.pop("name")

    # Act and Assert
    with pytest.raises(KeyError, match="name"):
        site = Site.from_dict(site_dict)


def test_from_dict_missing_latitude(valid_site_dict):
    # Arrange
    site_dict = copy.deepcopy(valid_site_dict)
    site_dict.pop("latitude")

    # Act and Assert
    with pytest.raises(KeyError, match="latitude"):
        site = Site.from_dict(site_dict)


def test_from_dict_with_extra_keys(valid_site_dict):
    # Arrange
    site_dict = copy.deepcopy(valid_site_dict)
    site_dict["extra_key"] = "extra_value"

    # Act
    site = Site.from_dict(site_dict)

    # Assert
    assert_site_matches_dict(site, valid_site_dict)


def test_to_dict_returns_correct_dict(one_saved_site):
    # Act
    site_dict = one_saved_site.to_dict()

    # Assert
    assert_dict_matches_site(one_saved_site, site_dict)


def test_to_dict_missing_id(one_saved_site):
    # Act
    site_dict = one_saved_site.to_dict()

    # Assert
    assert_dict_matches_site(one_saved_site, site_dict)


def test_to_dict_missing_latitude():
    # Arrange
    site = Site(
        name="Test Site",
        status=SiteStatus.OPEN,
        address_line1="603 3rd Ave SE",
        address_line2=None,
        city="Algona",
        state="WA",
        postal_code="98001",
        latitude=None,
        longitude=-122.236,
        phone="123-456-7890",
        eligibility=Eligibility.OLDER_ADULTS_AND_ELIGIBLE,
        hours={},
        service_notes="No notes",
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    # Act
    site_dict = site.to_dict()

    # Assert
    assert site_dict["latitude"] is None