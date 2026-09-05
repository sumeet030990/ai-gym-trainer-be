from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import attendance_repository
from db.schemas import UserAttendance


async def create_attendance(user_id: UUID, attendance_date: datetime, db_session: AsyncSession) -> UserAttendance:
    return await attendance_repository.create_attendance(user_id, attendance_date, db_session)


async def get_user_attendance(
    user_id: UUID,
    db_session: AsyncSession,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> list[UserAttendance]:
    return await attendance_repository.get_user_attendance(user_id, db_session, start_date, end_date)


async def get_owned_attendance_by_id(attendance_id: UUID, user_id: UUID, db_session: AsyncSession) -> UserAttendance:
    attendance = await attendance_repository.get_attendance_by_id(attendance_id, db_session)

    if not attendance or attendance.user_id != user_id:
        raise ValueError("Attendance record not found")

    return attendance


async def delete_attendance(attendance_id: UUID, user_id: UUID, db_session: AsyncSession) -> None:
    attendance = await get_owned_attendance_by_id(attendance_id, user_id, db_session)
    await attendance_repository.delete_attendance(attendance, db_session)
