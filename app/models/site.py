from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from ..db import db


class SiteStatus(str, Enum):
  OPEN = "open"
  CLOSED = "closed"

  @classmethod
  def from_frontend(cls, value: str) -> "SiteStatus":
    """Convert frontend format to SiteStatus enum"""
    mapping = {
      "Open": cls.OPEN,
      "Closed": cls.CLOSED
    }

    return mapping[value]

class Eligibility(str, Enum):
  GENERAL_PUBLIC = "general_public"
  OLDER_ADULTS_AND_ELIGIBLE = "older_adults_and_eligible"
  YOUTH_YOUNG_ADULTS = "youth_young_adults"

  @classmethod
  def from_frontend(cls, value: str) -> "Eligibility":
      """Convert frontend format to Eligibility enum"""
      mapping = {
          "General Public": cls.GENERAL_PUBLIC,
          "Older Adults 60+ and Eligible Participants": cls.OLDER_ADULTS_AND_ELIGIBLE,
          "Youth and Young Adults": cls.YOUTH_YOUNG_ADULTS
      }
      return mapping[value]

class Site(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  status: Mapped[SiteStatus] = mapped_column(default=SiteStatus.OPEN)
  address_line1: Mapped[str]
  address_line2: Mapped[Optional[str]]
  city: Mapped[str]
  state: Mapped[str]
  postal_code: Mapped[str]
  latitude: Mapped[Optional[float]]
  longitude: Mapped[Optional[float]]
  phone: Mapped[str]
  eligibility: Mapped[Eligibility]
  hours: Mapped[dict] = mapped_column(JSONB, default=dict)
  service_notes: Mapped[str]
  created_at: Mapped[datetime]
  updated_at: Mapped[Optional[datetime]]

  @classmethod
  def from_dict(cls, site_dict):
    return cls(
      name=site_dict["name"],
      status=SiteStatus.from_frontend(site_dict["status"]),
      address_line1=site_dict["address_line1"],
      address_line2=site_dict.get("address_line2"),
      city=site_dict["city"],
      state=site_dict["state"],
      postal_code=site_dict["postal_code"],
      latitude=site_dict.get("latitude"),
      longitude=site_dict.get("longitude"),
      phone=site_dict["phone"],
      eligibility=Eligibility.from_frontend(site_dict["eligibility"]),
      hours=site_dict["hours"],
      service_notes=site_dict.get("service_notes", ""),
      created_at=datetime.now(),
    )

