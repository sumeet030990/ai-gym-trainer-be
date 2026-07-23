
from fastapi import APIRouter, Depends
from db.database import get_session
from app.controllers import goal_questions_controller
from app.schemas.goal_questions_schemas import GoalQuestionsByCategoryResponse


router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/", response_model=list[GoalQuestionsByCategoryResponse])
async def get_all_questions(category_id: str|None = None, db_session=Depends(get_session)):
    return await goal_questions_controller.get_all_goal_questions(category_id, db_session)

