from datetime import datetime
from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  created_at: Mapped[datetime]