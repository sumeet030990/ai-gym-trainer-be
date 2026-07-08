import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class ExerciseEquipment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "exercise_equipment"

    exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exercises.id"), nullable=False, index=True)
    equipment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gym_equipments.id"), nullable=False, index=True)