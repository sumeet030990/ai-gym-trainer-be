from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas import Roles, Users


async def get_role_by_name(session: AsyncSession, name: str) -> Roles | None:
    stmt = select(Roles).where(Roles.name == name)
    return (await session.execute(stmt)).scalar_one_or_none()


async def get_by_mobile_no(session: AsyncSession, mobile_no: str) -> Users | None:
    stmt = select(Users).where(Users.mobile_no == mobile_no)
    return (await session.execute(stmt)).scalar_one_or_none()


async def get_by_email(session: AsyncSession, email: str) -> Users | None:
    stmt = select(Users).where(Users.email == email)
    return (await session.execute(stmt)).scalar_one_or_none()


async def create(session: AsyncSession, user: Users) -> Users:
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except Exception as e:
        await session.rollback()
        raise e


async def get_by_mobile_or_email(session: AsyncSession, user_name: str) -> Users | None:
    stmt = select(Users).where((Users.mobile_no == user_name) | (Users.email == user_name))
    return (await session.execute(stmt)).scalar_one_or_none()