from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.schemas import Muscles

async def get_all_muscles(db_session: AsyncSession) -> list[Muscles]:
    """Fetch all muscles with pagination."""
    result = await db_session.execute(select(Muscles))
    muscles = result.scalars().all()
    
    return list(muscles)