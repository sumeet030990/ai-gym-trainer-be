import uuid
from datetime import datetime

from pydantic import BaseModel

from db.schemas.goal_questions import QUESTION_TYPE


class CategoryResponse(BaseModel):
    id: uuid.UUID
    name: str

class GoalQuestionOptionResponse(BaseModel):
    id: uuid.UUID
    label: str
    sort_order: int | None
    
class GoalQuestionResponse(BaseModel):
    """Public representation of a goal question, including its nested category."""

    id: uuid.UUID
    question: str
    question_type: QUESTION_TYPE
    is_active: bool
    category: CategoryResponse | None
    sort_order: int | None
    options: list[GoalQuestionOptionResponse]

class GoalQuestionsByCategoryResponse(BaseModel):
    """Goal questions grouped by their category."""

    category: CategoryResponse | None
    questions: list[GoalQuestionResponse]
