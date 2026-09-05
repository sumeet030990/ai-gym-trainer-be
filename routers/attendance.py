from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from app.controllers import attendance_controller
from app.schemas.attendance_schemas import AttendanceCreateRequest, AttendanceResponseSchema
from core.security import is_user_authenticated
from db.database import get_session

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
)


@router.post("/", summary="Log a gym check-in for the authenticated user.")
async def create_attendance(
    request_data: AttendanceCreateRequest,
    auth_user=Depends(is_user_authenticated),
    db_session=Depends(get_session),
) -> AttendanceResponseSchema:
    return await attendance_controller.create_attendance(request_data, auth_user, db_session)


@router.get("/{user_id}", summary="Get the attendance history for the authenticated user.")
async def get_user_attendance(
    user_id: UUID,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    auth_user=Depends(is_user_authenticated),
    db_session=Depends(get_session),
) -> list[AttendanceResponseSchema]:
    return await attendance_controller.get_user_attendance(user_id, db_session, start_date, end_date)


@router.delete("/{attendance_id}", summary="Delete an attendance record belonging to the authenticated user.")
async def delete_attendance(
    attendance_id: UUID,
    auth_user=Depends(is_user_authenticated),
    db_session=Depends(get_session),
):
    return await attendance_controller.delete_attendance(attendance_id, auth_user, db_session)
