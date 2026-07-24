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