from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import excercise_services
from app.schemas.excercise_schemas import ExerciseSchema


async def get_all_exercises(
    db_session: AsyncSession,
    gym_id: Optional[uuid.UUID] = None,
)->list[ExerciseSchema]:
    """Get all exercises or as filtered by a specific gym based on the provided gym ID."""
    result =  await excercise_services.get_all_exercises(db_session, gym_id)
    
    return [ExerciseSchema.model_validate(exercise) for exercise in result]
  