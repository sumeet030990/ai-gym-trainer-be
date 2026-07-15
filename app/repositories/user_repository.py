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

async def update_user(db_session: AsyncSession, user: Users) -> Users:
    try:
        await db_session.commit()
        await db_session.refresh(user)
        return user
    except Exception as e:
        await db_session.rollback()
        raise e


async def delete_user(db_session: AsyncSession, user: Users) -> bool:
    try:
        await db_session.delete(user)
        await db_session.commit()
        return True
    except Exception as e:
        await db_session.rollback()
        raise e