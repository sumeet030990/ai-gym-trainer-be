
from fastapi import APIRouter, Depends
from db.database import get_session
from app.controllers import goal_questions_controller


router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/")
async def get_all_questions(db_session=Depends(get_session)):
    return await goal_questions_controller.get_all_goal_questions(db_session)

