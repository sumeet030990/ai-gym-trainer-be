from db.database import Base
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class WorkoutExerciseDetails(Base):
    __tablename__ = "workout_exercise_details"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    workout_exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workout_exercises.id"), nullable=False)
    target_sets: Mapped[int] = mapped_column(nullable=False)
    actual_sets: Mapped[int] = mapped_column(nullable=True)  # Actual sets can be optional
    target_reps: Mapped[int] = mapped_column(nullable=False)
    actual_reps: Mapped[int] = mapped_column(nullable=True)  # Actual reps can be optional
    target_weight: Mapped[float | None] = mapped_column(nullable=True)  # Target weight can be optional
    actual_weight: Mapped[float | None] = mapped_column(nullable=True)  # Actual weight can be optional