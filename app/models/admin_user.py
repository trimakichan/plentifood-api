from datetime import datetime
from typing import TYPE_CHECKING
from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from app.models.organization import Organization

class AdminUser(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), unique=True)
    organization: Mapped["Organization"] = relationship(back_populates="admin_user", uselist=False)
    created_at: Mapped[datetime]

    @classmethod
    def from_dict(cls, admin_dict):
        return cls(
            username=admin_dict["username"]
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