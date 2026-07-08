
from db.database import Base

import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey



class UserConditions(Base):
  __tablename__ = "user_conditions"
  
  id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
  condition_name: Mapped[str] = mapped_column(nullable=False)
  notes: Mapped[str | None] = mapped_column(nullable=True)