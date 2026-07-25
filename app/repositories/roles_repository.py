from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.roles import Roles
from sqlalchemy import select

async def get_all_roles(db_session: AsyncSession) -> list[Roles]:
    try:
        roles = await db_session.execute(select(Roles))
        roles = roles.scalars().all()
        
        return list(roles)
    except Exception as e:
        await db_session.rollback()
        raise e