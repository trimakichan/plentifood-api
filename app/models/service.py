from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .site import Site


class Service(db.Model):
  """Services will be created only by the developer. Seed the table by creating seeds/services.py"""
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
  name: Mapped[str]
  sites: Mapped[list["Site"]] = relationship(secondary="site_service", back_populates="services")


  # @classmethod
  # def from_dict(cls, service_data):
  #   return cls(name=service_data["name"])