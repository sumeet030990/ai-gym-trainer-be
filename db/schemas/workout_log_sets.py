import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class WorkoutLogSets(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workout_log_sets"

    workout_log_exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workout_log_exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    set_number: Mapped[int] = mapped_column(nullable=False)
    reps: Mapped[int] = mapped_column(nullable=False)
    weight_kg: Mapped[float] = mapped_column(nullable=False)
