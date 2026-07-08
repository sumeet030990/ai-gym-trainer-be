from db.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.sql import func

class Exercises(Base):
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    equipment_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("gym_equipments.id"), nullable=True)
    muscle_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("muscles.id"), nullable=True)
    video_url: Mapped[str | None] = mapped_column(nullable=True)
    video_provider  : Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())