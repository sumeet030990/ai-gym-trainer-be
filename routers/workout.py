

from fastapi import APIRouter, Depends
from app.controllers import workout_controller
from app.schemas.workout_schemas import WorkoutLogRequest
from core.security import is_user_authenticated

from db.database import get_session


router = APIRouter(
    prefix="/workout",
    tags=["workout"],
)

  
@router.post("/ai/generate-plan", summary="Generate a personalized workout plan based on user goals and preferences.")
async def generate_plan(auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):

  return await workout_controller.generate_plan(auth_user, db_session)


@router.get("/get-user-plan", summary="Get the personalized workout plan for the authenticated user.")
async def get_user_plan(auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await workout_controller.get_user_plan(auth_user, db_session)
  

@router.post("/log-workout", summary="Log a workout for the authenticated user.")
async def log_user_workout(request_data: WorkoutLogRequest, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session
)):
    return await workout_controller.log_user_workout(request_data, auth_user, db_session)
  