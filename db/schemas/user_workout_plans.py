import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class UserWorkoutPlans(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user_workout_plans"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    workout_plan: Mapped[dict] = mapped_column(JSONB, nullable=False)
