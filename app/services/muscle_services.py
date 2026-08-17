from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas import Muscles
from app.repositories import muscle_repository

async def get_all_muscles(db_session: AsyncSession) -> list[Muscles]:
    """Fetch all muscles with pagination."""
    return await muscle_repository.get_all_muscles(db_session)