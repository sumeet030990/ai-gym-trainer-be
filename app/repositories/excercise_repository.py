
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.schemas import Exercises, ExerciseEquipment, GymEquipments

async def get_all_exercises(db_session: AsyncSession, gym_id: uuid.UUID|None = None):
    query = select(Exercises).options(selectinload(Exercises.muscle))
    if gym_id is not None:
        primary_equipment_in_gym = (
            select(GymEquipments.id)
            .where(
                GymEquipments.id == Exercises.equipment_id,
                GymEquipments.gym_id == gym_id,
            )
            .exists()
        )
        extra_equipment_in_gym = (
            select(ExerciseEquipment.id)
            .join(GymEquipments, GymEquipments.id == ExerciseEquipment.equipment_id)
            .where(
                ExerciseEquipment.exercise_id == Exercises.id,
                GymEquipments.gym_id == gym_id,
            )
            .exists()
        )
        query = query.where(primary_equipment_in_gym | extra_equipment_in_gym)
    result = await db_session.execute(query)
    return result.scalars().all()