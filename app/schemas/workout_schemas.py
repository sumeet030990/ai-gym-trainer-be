from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class WorkoutSetLog(BaseModel):
    """A single completed set within an exercise."""
    set_number: int = Field(..., ge=1, description="Order of this set within the exercise.")
    reps: int = Field(..., ge=0, description="Reps completed in this set.")
    weight_kg: float = Field(..., ge=0, description="Weight used; 0 for bodyweight.")


class WorkoutExerciseLog(BaseModel):
    """An exercise performed, with its individual sets."""
    exercise_id: UUID = Field(..., description="ID of the exercise performed.")
    sets: list[WorkoutSetLog] = Field(..., min_length=1, description="Sets performed for this exercise.")


class WorkoutMuscleLog(BaseModel):
    """A muscle group trained, with the exercises performed for it."""
    muscle_id: UUID = Field(..., description="ID of the muscle group targeted.")
    exercises: list[WorkoutExerciseLog] = Field(..., min_length=1, description="Exercises performed for this muscle.")


class WorkoutLogRequest(BaseModel):
    """
    Schema for logging a completed workout session.
    """
    workout_date: date = Field(default_factory=date.today, description="Date the workout was performed.")
    muscles: list[WorkoutMuscleLog] = Field(..., min_length=1, description="Muscle groups trained, each with its exercises and sets.")
