from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas import Gyms
from sqlalchemy import select


async def get_all_gyms(db_session: AsyncSession, page: int, page_size: int) -> tuple[list[Gyms], int]:
    try:
        total = await db_session.execute(select(Gyms))
        total = total.scalars().all()
        total = len(total)
        result = await db_session.execute(
            select(Gyms)
            .offset((page - 1) * page_size).limit(page_size)
            .order_by(Gyms.created_at.desc())
        )
        gyms = result.scalars().all()
        return list(gyms), total
    except Exception as e:
        await db_session.rollback()
        raise e
      
async def get_gym_by_id(gym_id: str, db_session: AsyncSession) -> Gyms:
  try:
      result = await db_session.execute(select(Gyms).where(Gyms.id == gym_id))
      gym = result.scalars().first()
      
      if not gym:
          raise Exception(f"Gym with id {gym_id} not found")

      return gym
  except Exception as e:
      await db_session.rollback()
      raise e


async def create_gym(gym_data: dict, db_session: AsyncSession) -> Gyms:
    try:
        new_gym = Gyms(**gym_data)
        db_session.add(new_gym)
        await db_session.commit()
        await db_session.refresh(new_gym)

        return new_gym
    except Exception as e:
        await db_session.rollback()
        raise e
  
  
async def update_gym(gym_id: str, gym_data: dict, db_session: AsyncSession) -> Gyms:
    try:
        result = await db_session.execute(select(Gyms).where(Gyms.id == gym_id))
        gym = result.scalars().first()
        
        if not gym:
            raise Exception(f"Gym with id {gym_id} not found")
        
        for key, value in gym_data.items():
            setattr(gym, key, value)
        
        await db_session.commit()
        await db_session.refresh(gym)

        return gym
    except Exception as e:
        await db_session.rollback()
        raise e
    
async def delete_gym(gym_id: str, db_session: AsyncSession):
    try:
        result = await db_session.execute(select(Gyms).where(Gyms.id == gym_id))
        gym = result.scalars().first()
        
        if not gym:
            raise Exception(f"Gym with id {gym_id} not found")
        
        await db_session.delete(gym)
        await db_session.commit()

        return {"message": f"Gym with id {gym_id} has been deleted"}
    except Exception as e:
        await db_session.rollback()
        raise e
