from app.services import equipments_services
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all_equipments(db_session: AsyncSession, page: int, page_size: int):
    result = await equipments_services.get_all_equipments(db_session, page, page_size)
    return result