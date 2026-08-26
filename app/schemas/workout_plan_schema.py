from enum import Enum

from pydantic import BaseModel, Field


class ExerciseSchema(BaseModel):
    name: str
    sets: int
    reps: str
    weight_kg: float = Field(description="Kg; 0 for bodyweight")
    form_cue: str
    sort_order: int


class WorkoutDaySchema(BaseModel):
    day: str
    muscles: list[str] = Field(description="1-2 muscle groups trained this day, from the fixed list")
    exercises: list[ExerciseSchema]
    warm_up: list[str] = Field(description="Warm-up routine for the day as per the targeted muscles; not a plan-wide warm-up")
    post_exercise_stretch: list[str] = Field(description="Stretching routine for the day as per the targeted muscles; not a plan-wide cool-down")
    notes: str | None = Field(default=None, description="Rationale for this day's exercise/muscle choices")


class WorkoutPlanSchema(BaseModel):
    days: list[WorkoutDaySchema]
    notes: str | None = Field(default=None, description="Plan-wide rationale, e.g. split/day-count decisions")
