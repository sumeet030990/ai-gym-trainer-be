from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import gym_equipments_repository
from app.schemas.gym_equipments_schemas import AssignGymEquipmentRequest

async def get_gym_equipments(gym_id: str, db_session: AsyncSession):
    return await gym_equipments_repository.get_gym_equipments(gym_id, db_session)


async def assign_gym_equipment(gym_id: str, payload: AssignGymEquipmentRequest, db_session: AsyncSession):
    return await gym_equipments_repository.assign_gym_equipment(gym_id, payload, db_session)