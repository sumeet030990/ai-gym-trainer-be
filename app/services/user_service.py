from fastapi import Depends

from app.repositories import user_repository, auth_repository
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session


async def get_all_users(db_session: AsyncSession, page: int, page_size: int):
    return await user_repository.get_all_users(db_session, page, page_size)

async def get_user_by_mobile_or_email(user_name: str, db_session: AsyncSession = Depends(get_session)):
    return await auth_repository.get_by_mobile_or_email(db_session, user_name)

async def get_user_by_id(id: str, db_session: AsyncSession):
    return await user_repository.get_user_by_id(db_session, id)