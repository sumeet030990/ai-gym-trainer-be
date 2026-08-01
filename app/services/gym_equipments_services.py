from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import gym_equipments_repository

async def get_gym_equipments(gym_id: str, db_session: AsyncSession):
    return await gym_equipments_repository.get_gym_equipments(gym_id, db_session)