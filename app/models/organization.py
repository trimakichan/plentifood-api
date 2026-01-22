from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from enum import Enum
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from app.models.site import Site
    from app.models.admin_user import AdminUser

class OrgType(str, Enum):
    FOOD_TYPE = "food_bank"
    CHURCH = "church"
    COMMUNITY_CENTER = "community_center"
    NON_PROFIT = "non_profit"
    OTHERS = "others"

    @classmethod
    def from_frontend(cls, value: str) -> "OrgType":
        """Convert frontend format to OrgType"""
        mapping = {
            "foodBank": cls.FOOD_TYPE,
            "church": cls.CHURCH,
            "communityCenter": cls.COMMUNITY_CENTER,
            "nonProfit": cls.NON_PROFIT,
            "others": cls.OTHERS
        }
        return mapping[value]

class Organization(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    organization_type: Mapped[OrgType] 
    website_url: Mapped[Optional[str]] = mapped_column(String(255))
    sites: Mapped[list["Site"]] = relationship(
        "Site",
        back_populates='organization',
        order_by="Site.id",
        cascade="all, delete-orphan"
    )
    admin_user: Mapped["AdminUser"] = relationship(
        back_populates="organization",
        uselist=False,
        cascade="save-update, merge"
    )
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]]

    @classmethod
    def from_dict(cls, organization_dict):
        return cls(
            name=organization_dict["name"],
            organization_type=OrgType.from_frontend(organization_dict["organization_type"]),
            website_url=organization_dict.get("website"),
            created_at=datetime.now(timezone.utc)
        )

    def to_dict(self):
        organization_dict = {
            "id": self.id,
            "name": self.name,
            "organization_type": self.organization_type,
            "website_url": self.website_url,
            "sites": [site.to_dict() for site in self.sites],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        return organization_dict