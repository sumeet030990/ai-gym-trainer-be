

from datetime import date



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

    workout_plan = await workout_services.get_user_workout_plan(user_details, db_session)
    return workout_plan