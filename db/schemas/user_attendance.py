import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class UserAttendance(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "user_attendance"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    attendance_date: Mapped[datetime] = mapped_column(nullable=False, index=True)
