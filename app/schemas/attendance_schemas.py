import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AttendanceCreateRequest(BaseModel):
    """Request body for POST /attendance."""

    attendance_date: datetime = Field(default_factory=_utcnow, description="When the user checked in at the gym.")

    @field_validator("attendance_date")
    @classmethod
    def attendance_date_not_in_future(cls, value: datetime) -> datetime:
        now = _utcnow() if value.tzinfo else _utcnow().replace(tzinfo=None)
        if value > now:
            raise ValueError("attendance_date cannot be in the future")
        return value


class AttendanceResponseSchema(BaseModel):
    """Public representation of an attendance record."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    attendance_date: datetime
    created_at: datetime
