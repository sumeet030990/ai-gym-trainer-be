

from datetime import date, datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.goal_questions_schemas import GoalQuestionOptionResponse
from app.schemas.role_schemas import RoleResponseSchema
from app.schemas.user_goal_answers_schema import UserAnswerSchema


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