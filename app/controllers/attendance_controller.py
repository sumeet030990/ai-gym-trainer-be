from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.attendance_schemas import AttendanceCreateRequest, AttendanceResponseSchema
from app.schemas.auth_schemas import UserRegisterResponse
from app.services import attendance_services, user_services


async def create_attendance(
    request_data: AttendanceCreateRequest, auth_user: UserRegisterResponse, db_session: AsyncSession
) -> AttendanceResponseSchema:
    """Log a gym check-in for the authenticated user."""
    user_details = await user_services.get_auth_user_details(auth_user, db_session)
    user = user_details["user"]

    attendance = await attendance_services.create_attendance(user.id, request_data.attendance_date, db_session)
    return AttendanceResponseSchema.model_validate(attendance)


async def get_user_attendance(
    user_id: UUID,
    db_session: AsyncSession,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> list[AttendanceResponseSchema]:
    """Get the attendance history for the authenticated user."""
    attendance_records = await attendance_services.get_user_attendance(user_id, db_session, start_date, end_date)
    return [AttendanceResponseSchema.model_validate(record) for record in attendance_records]


async def delete_attendance(attendance_id: UUID, auth_user: UserRegisterResponse, db_session: AsyncSession) -> dict:
    """Delete an attendance record belonging to the authenticated user."""
    user_details = await user_services.get_auth_user_details(auth_user, db_session)
    user = user_details["user"]

    await attendance_services.delete_attendance(attendance_id, user.id, db_session)
    return {"message": "Attendance record deleted successfully"}
