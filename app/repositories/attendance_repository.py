from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.schemas import UserAttendance


async def create_attendance(user_id: UUID, attendance_date: datetime, db_session: AsyncSession) -> UserAttendance:
    try:
        if attendance_date.tzinfo is not None:
            attendance_date = attendance_date.astimezone(timezone.utc).replace(tzinfo=None)

        new_attendance = UserAttendance(user_id=user_id, attendance_date=attendance_date)
        db_session.add(new_attendance)
        await db_session.commit()
        await db_session.refresh(new_attendance)

        return new_attendance
    except Exception as e:
        await db_session.rollback()
        raise e


async def get_user_attendance(
    user_id: UUID,
    db_session: AsyncSession,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> list[UserAttendance]:
    query = select(UserAttendance).where(UserAttendance.user_id == user_id)

    if start_date:
        query = query.where(UserAttendance.attendance_date >= start_date)
    else:
        thirty_days_ago = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=30)
        query = query.where(UserAttendance.attendance_date >= thirty_days_ago)

    if end_date:
        query = query.where(UserAttendance.attendance_date <= end_date)
    else:
        query = query.where(UserAttendance.attendance_date <= datetime.now(timezone.utc).replace(tzinfo=None))

    result = await db_session.execute(query.order_by(UserAttendance.attendance_date.desc()))
    return list(result.scalars().all())


async def get_attendance_by_id(attendance_id: UUID, db_session: AsyncSession) -> Optional[UserAttendance]:
    result = await db_session.execute(select(UserAttendance).where(UserAttendance.id == attendance_id))
    return result.scalars().first()


async def delete_attendance(attendance: UserAttendance, db_session: AsyncSession) -> None:
    try:
        await db_session.delete(attendance)
        await db_session.commit()
    except Exception as e:
        await db_session.rollback()
        raise e
