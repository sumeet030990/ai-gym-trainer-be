from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import gym_repository

async def get_all_gyms(db_session: AsyncSession, page: int = 1, page_size: int = 10):
    return await gym_repository.get_all_gyms(db_session, page, page_size)