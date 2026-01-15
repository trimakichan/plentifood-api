from app.models.site import Eligibility, Site, SiteStatus
from app.db import db
from datetime import datetime
import pytest
import copy


def test_from_dict_returns_site(valid_site_dict):
    # Arrange

    # Act
    site = Site.from_dict(valid_site_dict)
    # Assert
    assert site.name == valid_site_dict["name"]
    assert site.status == SiteStatus.OPEN
    assert isinstance(site.status, SiteStatus)
    assert site.address_line1 == valid_site_dict["address_line1"]
    assert site.address_line2 is None
    assert site.city == valid_site_dict["city"]
    assert site.state == valid_site_dict["state"]
    assert site.postal_code == valid_site_dict["postal_code"]
    assert site.latitude == valid_site_dict["latitude"]
    assert site.longitude == valid_site_dict["longitude"]
    assert site.phone == valid_site_dict["phone"]
    assert site.eligibility == Eligibility.OLDER_ADULTS_AND_ELIGIBLE
    assert isinstance(site.eligibility, Eligibility)
    assert site.hours == valid_site_dict["hours"]
    assert site.service_notes == valid_site_dict["service_notes"]
    assert site.created_at is not None
    assert site.updated_at is None


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
    assert site.name == valid_site_dict["name"]
    assert site.status == SiteStatus.OPEN
    assert isinstance(site.status, SiteStatus)
    assert site.address_line1 == valid_site_dict["address_line1"]
    assert site.address_line2 is None
    assert site.city == valid_site_dict["city"]
    assert site.state == valid_site_dict["state"]
    assert site.postal_code == valid_site_dict["postal_code"]
    assert site.latitude == valid_site_dict["latitude"]
    assert site.longitude == valid_site_dict["longitude"]
    assert site.phone == valid_site_dict["phone"]
    assert site.eligibility == Eligibility.OLDER_ADULTS_AND_ELIGIBLE
    assert isinstance(site.eligibility, Eligibility)
    assert site.hours == valid_site_dict["hours"]
    assert site.service_notes == valid_site_dict["service_notes"]
    assert site.created_at is not None
    assert site.updated_at is None


def test_to_dict_returns_correct_dict(valid_site):
    # Arrange

    # Act
    site_dict = valid_site.to_dict()

    # Assert
    assert site_dict["id"] is None
    assert site_dict["name"] == valid_site.name
    assert site_dict["status"] == SiteStatus.OPEN.value
    assert site_dict["address_line1"] == valid_site.address_line1
    assert site_dict["address_line2"] is None
    assert site_dict["city"] == valid_site.city
    assert site_dict["state"] == valid_site.state
    assert site_dict["postal_code"] == valid_site.postal_code
    assert site_dict["latitude"] == valid_site.latitude
    assert site_dict["longitude"] == valid_site.longitude
    assert site_dict["phone"] == valid_site.phone
    assert site_dict["eligibility"] == Eligibility.OLDER_ADULTS_AND_ELIGIBLE.value
    assert site_dict["hours"] == valid_site.hours
    assert site_dict["service_notes"] == valid_site.service_notes
    assert isinstance(site_dict["created_at"], str)
    assert site_dict["updated_at"] is None


def test_to_dict_missing_id(valid_site):
    # Arrange

    # Act
    result = valid_site.to_dict()

    # Assert
    assert result["id"] is None
    assert result["name"] == valid_site.name
    assert result["status"] == SiteStatus.OPEN.value
    assert result["eligibility"] == Eligibility.OLDER_ADULTS_AND_ELIGIBLE.value
    assert result["address_line2"] is None
    assert result["hours"] == valid_site.hours
    assert isinstance(result["created_at"], str)
    assert result["updated_at"] is None


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
        created_at=datetime.now(),
        updated_at=None,
    )

    # Act
    result = site.to_dict()

    # Assert
    assert result["latitude"] is None
