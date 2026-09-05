

from datetime import date
from typing import Optional

from app.schemas.workout_schemas import WorkoutLogRequest
from app.services import workout_services
from app.schemas.auth_schemas import UserRegisterResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import user_services
import os



async def generate_plan(auth_user: UserRegisterResponse, db_session: AsyncSession):
    """Generate a personalized workout plan based on user goals and preferences."""
    user_details = await user_services.get_auth_user_details(auth_user, db_session)

    if not user_details:
        raise ValueError("User not found")

    workout_plan = await workout_services.generate_workout_plan(user_details, db_session)

    saved_plan = await workout_services.save_workout_plan(user_details, workout_plan, db_session)
    return saved_plan


async def get_user_plan(auth_user: UserRegisterResponse, db_session: AsyncSession):
    """Get the personalized workout plan for the authenticated user."""
    user_details = await user_services.get_auth_user_details(auth_user, db_session)

    if not user_details:
        raise ValueError("User not found")
    user = user_details["user"]
        
    workout_plan = await workout_services.get_user_workout_plan(user.id, db_session)
    return workout_plan

# =====================================
async def get_user_workout_logs(auth_user: UserRegisterResponse, db_session: AsyncSession, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Get the workout logs for the authenticated user."""
    user_details = await user_services.get_auth_user_details(auth_user, db_session)

    if not user_details:
        raise ValueError("User not found")
    user = user_details["user"]

    return await workout_services.get_user_workout_logs(user.id, db_session, start_date, end_date)

async def log_user_workout(request_data: WorkoutLogRequest, auth_user: UserRegisterResponse, db_session: AsyncSession):
    """Log a completed workout for the authenticated user."""
    user_details = await user_services.get_auth_user_details(auth_user, db_session)

    if not user_details:
        raise ValueError("User not found")
    
    return await workout_services.log_workout(auth_user.id, request_data, db_session)