
from pydantic import BaseModel
import uuid

class UserAnswerSchema(BaseModel):
    option_id: uuid.UUID | None
    answer_text: str | None

class UserGoalAnswerQuestionSchema(BaseModel):
    question_id: uuid.UUID
    answers: list[UserAnswerSchema]
class UserGoalAnswersRequestSchema(BaseModel):
    user_goals: list[UserGoalAnswerQuestionSchema]
   