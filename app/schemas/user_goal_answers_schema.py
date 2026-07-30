
from pydantic import BaseModel, ConfigDict
import uuid

class UserAnswerSchema(BaseModel):
    option_id: uuid.UUID | None
    answer_text: str | None

class UserGoalAnswerQuestionSchema(BaseModel):
    question_id: uuid.UUID
    answers: list[UserAnswerSchema]
class UserGoalAnswersRequestSchema(BaseModel):
    user_goals: list[UserGoalAnswerQuestionSchema]
    
    
class GoalOptionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    sort_order: int
    label: str

class UserGoalAnswerItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    answer_text: str | None
    option: GoalOptionResponseSchema | None
class GoalQuestionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    question: str
    question_type: str
    sort_order: int | None
class UserGoalAnswerGroupSchema(BaseModel):
    question: GoalQuestionResponseSchema
    answers: list[UserGoalAnswerItemSchema]