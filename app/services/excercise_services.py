from app.repositories import excercise_repository
import uuid
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_exercises(db_session: AsyncSession, gym_id: uuid.UUID|None = None):
  return await excercise_repository.get_all_exercises(db_session, gym_id)