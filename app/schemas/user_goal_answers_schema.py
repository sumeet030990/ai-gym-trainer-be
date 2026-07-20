
from pydantic import BaseModel
import uuid

class UserAnswerSchema(BaseModel):
    option_id: uuid.UUID | None
    answer_text: str | None
    
class UserGoalAnswersRequestSchema(BaseModel):
    question_id: uuid.UUID
    answers: list[UserAnswerSchema]
   