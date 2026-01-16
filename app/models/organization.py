from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from enum import Enum
from typing import Optional
from ..db import db
from app.models.admin_user import AdminUser


class OrgType(str, Enum):
    FOOD_TYPE = "food_bank"
    CHURCH = "church"
    COMMUNITY_CENTER = "community_center"
    NON_PROFIT = "non_profit"
    OTHERS = "others"

    # FoodBank -> food_back
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
    name: Mapped[str] = mapped_column(String[100])
    organization_type: Mapped[OrgType] 
    website_url: Mapped[Optional[str]] = mapped_column(String(255))
    sites: Mapped[list["Site"]] = relationship(
        "Site",
        back_populates='organization',
        order_by="Site.id"
    )
    admin_user: Mapped["AdminUser"] = relationship(back_populates="organization", uselist=False)

    @classmethod
    def from_dict(cls, organization_dict):
        return cls(
            name=organization_dict["name"],
            organization_type=OrgType.from_frontend(organization_dict["organization_type"])
        )

    def to_dict(self):
        organization_dict = {
            "organization_id": self.organization_id,
            "name": self.name,
            "organization_type": self.organization_type,
            "website_url": self.website_url,
            "sites": [site.to_dict() for site in self.sites]
        }
        return organization_dict