

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas import UserGyms


async def assign_user_to_gym(gym_id: str, payload: dict, db_session: AsyncSession):
  try:
    await db_session.execute(delete(UserGyms).where(UserGyms.gym_id == gym_id))
    gym_users = payload.get("gym_users", [])
    for user_data in gym_users:
        db_session.add(UserGyms(user_id=user_data["user_id"], trainer_id=user_data.get("trainer_id") or None, gym_id=gym_id))

    await db_session.commit()
    
    return {"message": "Users assigned to gym successfully."}
  except Exception as e:
    await db_session.rollback()
    raise e