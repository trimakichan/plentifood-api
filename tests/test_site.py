from app.models.site import Eligibility, Site, SiteStatus
from app.db import db
import pytest

def test_site_from_dict():
  # Arrange
  site_dict = {
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
      "sunday":    [{ "open": "10:00", "close": "14:00" }],
      "monday":    [{ "open": "10:00", "close": "14:00" }],
      "tuesday":   [{ "open": "10:00", "close": "14:00" }],
      "wednesday": [],
      "thursday":  [{ "open": "12:00", "close": "16:00" }],
      "friday":    [{ "open": "10:00", "close": "13:00" }],
      "saturday":  []
},
    "service_notes": "No special notes",
  }

  # Act
  site = Site.from_dict(site_dict)
  # Assert
  assert site.name == site_dict["name"]
  assert site.status == SiteStatus.OPEN
  assert isinstance(site.status, SiteStatus)
  assert site.address_line1 == site_dict["address_line1"]
  assert site.address_line2 is None
  assert site.city == site_dict["city"]
  assert site.state == site_dict["state"]
  assert site.postal_code == site_dict["postal_code"]
  assert site.latitude == site_dict["latitude"]
  assert site.longitude == site_dict["longitude"]
  assert site.phone == site_dict["phone"]
  assert site.eligibility == Eligibility.OLDER_ADULTS_AND_ELIGIBLE
  assert isinstance(site.eligibility, Eligibility)
  assert site.hours == site_dict["hours"]
  assert site.service_notes == site_dict["service_notes"]
  assert site.created_at is not None
  assert site.updated_at is None