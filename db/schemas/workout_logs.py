import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class WorkoutLogs(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workout_logs"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    attendance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_attendance.id", ondelete="CASCADE"), nullable=False, index=True)
