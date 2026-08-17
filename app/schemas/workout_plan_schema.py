from enum import Enum

from pydantic import BaseModel, Field


class ExerciseSchema(BaseModel):
    name: str
    sets: int
    reps: str
    weight_kg: float = Field(description="Suggested load in kilograms; 0 for bodyweight-only exercises")
    form_cue: str
    sort_order: int = Field(description="Order of the exercise in the workout plan")
    notes: str | None = Field(default=None, description="Additional notes or recommendations for the exercise")


class WorkoutDaySchema(BaseModel):
    day: str
    muscles: list[str] = Field(description="One or two muscle groups trained this day, from the fixed muscle list")
    exercises: list[ExerciseSchema]
    warm_up_stretches: list[str] | None = Field(default=None, description="Suggested warm-up stretches for the exercise")
    post_exercise_stretches: list[str] | None = Field(default=None, description="Suggested post-exercise stretches for the exercise")
    notes: str | None = Field(default=None, description="Additional notes or recommendations for the workout day")


class WorkoutPlanSchema(BaseModel):
    days: list[WorkoutDaySchema]
    notes: str | None = Field(default=None, description="Additional notes or recommendations for the workout plan")
