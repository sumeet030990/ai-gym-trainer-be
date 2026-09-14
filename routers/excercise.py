

import uuid

from fastapi import APIRouter, Depends
from app.controllers import excercise_controller
from core.security import is_user_authenticated
from db.database import get_session

router = APIRouter(
  prefix="/exercise",
  tags=["exercise"]
)


@router.get("/")
async def get_all_exercises(db_session=Depends(get_session), gym_id: uuid.UUID|None = None, auth_user=Depends(is_user_authenticated)):
    return await excercise_controller.get_all_exercises(db_session, gym_id)