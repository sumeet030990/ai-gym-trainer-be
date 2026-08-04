from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.gym_equipments_schemas import AssignGymEquipmentRequest
from db.schemas import GymEquipments
from sqlalchemy.future import select
from sqlalchemy import delete, insert
from sqlalchemy.orm import selectinload

async def get_gym_equipments(gym_id: str, db_session: AsyncSession):
    result = await db_session.execute(
        select(GymEquipments).where(GymEquipments.gym_id == gym_id).options(selectinload(GymEquipments.equipment))
    )
    return result.scalars().all()

async def assign_gym_equipment(gym_id: str, payload: AssignGymEquipmentRequest, db_session: AsyncSession):
    try:
        await db_session.execute(
            delete(GymEquipments).where(GymEquipments.gym_id == gym_id)
        )

        if not payload.equipments:
            await db_session.commit()
            return []

        result = await db_session.execute(
            insert(GymEquipments).returning(GymEquipments),
            [{"gym_id": gym_id, "equipment_id": equipment_id} for equipment_id in payload.equipments]
        )
        gym_equipments = list(result.scalars().all())

        await db_session.commit()

        return gym_equipments
    except Exception as e:
        await db_session.rollback()
        raise e