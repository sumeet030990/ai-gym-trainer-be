

from sqlalchemy.ext.asyncio import AsyncSession
from app.services import gym_services

async def get_all_gyms(db_session: AsyncSession, page: int = 1, page_size: int = 10):
    return await gym_services.get_all_gyms(db_session, page, page_size)