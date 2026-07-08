from db.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class GymEquipments(Base):
  __tablename__ = "gym_equipments"
  id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
  gym_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gyms.id"), nullable=False)
  name: Mapped[str] = mapped_column(nullable=False)
  description: Mapped[str | None] = mapped_column(nullable=True)
  is_active: Mapped[bool] = mapped_column(nullable=False, default=True)