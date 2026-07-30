
from app.repositories import equipments_repository
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all_equipments(db_session: AsyncSession, page: int, page_size: int):
    result = await equipments_repository.get_all_equipments(db_session, page, page_size)
    return result