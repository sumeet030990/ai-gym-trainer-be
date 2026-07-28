

from sqlalchemy.ext.asyncio import AsyncSession
from app.services import gym_services, user_services, user_gym_services
from db.schemas.gyms import Gyms

async def get_all_gyms(db_session: AsyncSession, page: int = 1, page_size: int = 10):
    return await gym_services.get_all_gyms(db_session, page, page_size)

async def get_gym_by_id(gym_id: str, db_session: AsyncSession)->Gyms:
    return await gym_services.get_gym_by_id(gym_id, db_session)

async def create_gym(gym_data: dict, db_session: AsyncSession)->Gyms:
    return await gym_services.create_gym(gym_data, db_session)


async def update_gym(gym_id: str, gym_data: dict, db_session: AsyncSession)->Gyms:
    return await gym_services.update_gym(gym_id, gym_data, db_session)


async def delete_gym(gym_id: str, db_session: AsyncSession):
    return await gym_services.delete_gym(gym_id, db_session)

async def get_gym_users(gym_id: str, user_role_id: str | None, db_session: AsyncSession):
    return await user_services.get_gym_users(gym_id, user_role_id, db_session)

async def assign_user_to_gym(gym_id: str, payload: dict, db_session: AsyncSession):
    return await user_gym_services.assign_user_to_gym(gym_id, payload, db_session)