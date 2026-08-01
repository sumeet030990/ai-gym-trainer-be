from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas import GymEquipments
from sqlalchemy.orm import selectinload

async def get_gym_equipments(gym_id: str, db_session: AsyncSession):
    result = await db_session.execute(
        select(GymEquipments).where(GymEquipments.gym_id == gym_id).options(selectinload(GymEquipments.equipment))
    )
    return result.scalars().all()
from sqlalchemy.future import select