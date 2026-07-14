from fastapi import Depends

from app.repositories import user_repository, auth_repository
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session


def get_all_users():
    return user_repository.get_all_users()

async def get_user_by_mobile_or_email(user_name: str, db_session: AsyncSession = Depends(get_session)):
    return await auth_repository.get_by_mobile_or_email(db_session, user_name)