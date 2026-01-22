from datetime import datetime
from typing import TYPE_CHECKING, Optional
from datetime import datetime, timezone
from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func

if TYPE_CHECKING:
    from app.models.organization import Organization

class AdminUser(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    organization_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organization.id"), unique=True)
    organization: Mapped["Organization"] = relationship(back_populates="admin_user", uselist=False)
    created_at: Mapped[datetime]
    #  = mapped_column(server_default=func.now())

    @classmethod
    def from_dict(cls, admin_dict):
        return cls(
            username=admin_dict["username"],
            created_at=datetime.now(timezone.utc)
        )

    def to_dict(self):
        admin_dict = {
            "id": self.id,
            "organization_id": self.organization_id,
            "username": self.username,
            "created_at": self.created_at.isoformat(),
        }
        return admin_dict