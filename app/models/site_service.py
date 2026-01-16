from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from ..db import db


class SiteService(db.Model):
    __tablename__ = "site_service"

    site_id: Mapped[int] = mapped_column(ForeignKey("site.id"), primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), primary_key=True)
