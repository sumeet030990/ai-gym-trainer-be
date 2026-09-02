import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class WorkoutLogExercises(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workout_log_exercises"

    workout_log_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workout_logs.id", ondelete="CASCADE"), nullable=False, index=True)
    # Muscle the exercise was logged under for this session; a given exercise can
    # be logged under different muscles across sessions (e.g. a compound lift).
    muscle_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("muscles.id", ondelete="SET NULL"), nullable=True, index=True)
    # No ondelete here on purpose: deleting an exercise shouldn't silently erase workout history.
    exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exercises.id"), nullable=False, index=True)
