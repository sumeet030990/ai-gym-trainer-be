from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import gym_repository

async def get_all_gyms(db_session: AsyncSession, page: int = 1, page_size: int = 10):
    return await gym_repository.get_all_gyms(db_session, page, page_size)
  
  
async def get_gym_by_id(gym_id: str, db_session: AsyncSession):
    return await gym_repository.get_gym_by_id(gym_id, db_session)

async def create_gym(gym_data: dict, db_session: AsyncSession):
    return await gym_repository.create_gym(gym_data, db_session)

async def update_gym(gym_id: str, gym_data: dict, db_session: AsyncSession):
    return await gym_repository.update_gym(gym_id, gym_data, db_session)

async def delete_gym(gym_id: str, db_session: AsyncSession):
    return await gym_repository.delete_gym(gym_id, db_session)
