from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.organization import Organization

if TYPE_CHECKING:
    from .service import Service

from ..db import db


class SiteStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"

    # @classmethod
    # def from_frontend(cls, value: str) -> "SiteStatus":
    #     """Convert frontend format to SiteStatus enum"""
    #     return cls(value)


class Eligibility(str, Enum):
    GENERAL_PUBLIC = "general_public"
    OLDER_ADULTS_AND_ELIGIBLE = "older_adults_and_eligible"
    YOUTH_YOUNG_ADULTS = "youth_young_adults"
    
class Site(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    status: Mapped[SiteStatus] = mapped_column(default=SiteStatus.OPEN)
    address_line1: Mapped[str]
    address_line2: Mapped[Optional[str]]
    city: Mapped[str]
    state: Mapped[str]
    postal_code: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    phone: Mapped[str]
    eligibility: Mapped[Eligibility]
    hours: Mapped[dict] = mapped_column(JSONB, default=dict)
    service_notes: Mapped[str]
    services: Mapped[list["Service"]] = relationship(
        secondary="site_service", back_populates="sites"
    )
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["Organization"] = relationship("Organization", back_populates="sites")
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]]

    @classmethod
    def from_dict(cls, site_dict, org_id):

        DAYS_OF_WEEK = [
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
        ]

        hours = site_dict.get("hours")
        if not isinstance(hours, dict) or set(hours.keys()) != set(DAYS_OF_WEEK):
            raise KeyError("hours")

        return cls(
            name=site_dict["name"],
            status=SiteStatus.OPEN, 
            address_line1=site_dict["address_line1"],
            address_line2=site_dict.get("address_line2"),
            city=site_dict["city"],
            state=site_dict["state"],
            postal_code=site_dict["postal_code"],
            latitude=site_dict["latitude"],
            longitude=site_dict["longitude"],
            phone=site_dict["phone"],
            eligibility=Eligibility(site_dict["eligibility"]),
            hours=site_dict["hours"],
            service_notes=site_dict.get("service_notes", ""),
            organization_id=org_id,
            created_at=datetime.now(timezone.utc),
        )

    def to_dict(self):
        site_as_dict = {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone": self.phone,
            "eligibility": self.eligibility.value,
            "hours": self.hours,
            "service_notes": self.service_notes,
            "services": [service.to_dict() for service in self.services],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        return site_as_dict

