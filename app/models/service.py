from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import Enum as SQLEnum

if TYPE_CHECKING:
    from .site import Site

class ServiceType(str, Enum):
    FOOD_BANK = "food_bank"
    MEAL = "meal"
    
class Service(db.Model):
    """Services will be created only by the developer. Seed the table by creating seeds/services.py"""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[ServiceType] = mapped_column(SQLEnum(
        ServiceType,
        values_callable = lambda enum_class: [member.value for member in enum_class],
        name="servicetype",
    ),
    nullable=False)
    sites: Mapped[list["Site"]] = relationship(
        secondary="site_service", back_populates="services"
    )

    @classmethod
    def from_dict(cls, service_data):
        return cls(name=service_data["name"])
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
