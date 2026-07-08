from db.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class ExerciseEquipment(Base):
    __tablename__ = "exercise_equipment"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exercises.id"), nullable=False)
    equipment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gym_equipments.id"), nullable=False)