from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user_gym_repository

async def assign_user_to_gym(gym_id: str, payload: dict, db_session: AsyncSession):
    return await user_gym_repository.assign_user_to_gym(gym_id, payload, db_session)