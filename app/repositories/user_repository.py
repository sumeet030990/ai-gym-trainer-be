from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas.users import Users


async def get_all_users(db_session: AsyncSession, page: int, page_size: int) -> tuple[list[Users], int]:
    total_items = await db_session.scalar(select(func.count()).select_from(Users))

    result = await db_session.execute(
        select(Users).order_by(Users.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    )

    return list(result.scalars().all()), total_items or 0

async def get_user_by_id(db_session: AsyncSession, id: str) -> Users | None:
    result = await db_session.execute(select(Users).where(Users.id == id))
    return result.scalar_one_or_none()