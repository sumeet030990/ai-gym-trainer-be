

from fastapi import APIRouter, Depends
from app.controllers import ai_controller
from core.security import is_user_authenticated

from db.database import get_session


router = APIRouter(
    prefix="/ai",
    tags=["ai"],
)


@router.post("/generate-plan", summary="Generate a personalized workout plan based on user goals and preferences.")
async def generate_plan(auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):

  return await ai_controller.generate_plan(auth_user, db_session)