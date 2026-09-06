

from datetime import date, datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.goal_questions_schemas import GoalQuestionOptionResponse
from app.schemas.role_schemas import RoleResponseSchema
from app.schemas.user_goal_answers_schema import UserAnswerSchema, UserGoalAnswerGroupSchema


class UserRegisterResponse(BaseModel):
    """Public representation of a newly registered user. Never includes the password/hash."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: RoleResponseSchema
    mobile_no: str
    email: str | None
    first_name: str | None
    last_name: str | None
    birth_date: date | None
    diet_type: str | None
    sex: str | None
    created_at: datetime

class UserGoalsDetailsResponse(BaseModel):
    """Public representation of a user's goals."""

    model_config = ConfigDict(from_attributes=True)

    question: GoalQuestionOptionResponse
    answers: list[UserAnswerSchema]


class UserConditionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    condition_name: str
    notes: str | None
    created_at: datetime


class BodyMeasurementResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    weight_kg: float | None
    height_cm: float | None
    chest_cm: float | None
    waist_cm: float | None
    hips_cm: float | None
    left_arm_cm: float | None
    right_arm_cm: float | None
    left_thigh_cm: float | None
    right_thigh_cm: float | None
    neck_cm: float | None
    body_fat_percent: float | None
    created_at: datetime


class UserSubscriptionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subscription_plan_id: uuid.UUID
    start_date: datetime
    end_date: datetime | None
    status: str


class AuthUserDetailSchema(BaseModel):
    """Public representation of the authenticated user's own profile. Never includes the password hash."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: RoleResponseSchema
    mobile_no: str
    email: str | None
    first_name: str | None
    last_name: str | None
    birth_date: date | None
    diet_type: str | None
    sex: str | None
    current_plan_id: uuid.UUID | None
    is_regeneration_required: bool
    last_regeneration_check: datetime | None
    created_at: datetime
    updated_at: datetime
    health_conditions: list[UserConditionResponseSchema]
    body_measurements: list[BodyMeasurementResponseSchema]
    subscriptions: list[UserSubscriptionResponseSchema]


class AuthUserDetailsResponse(BaseModel):
    user: AuthUserDetailSchema
    user_goals: list[UserGoalAnswerGroupSchema]