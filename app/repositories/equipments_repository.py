
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.schemas import Equipments

async def get_all_equipments(db_session: AsyncSession, page: int, page_size: int):
    result = await db_session.execute(
        select(Equipments)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return list(result.scalars().all())