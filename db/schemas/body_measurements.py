import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class BodyMeasurements(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "body_measurements"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    trainer_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    gym_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("gyms.id", ondelete="SET NULL"), nullable=True, index=True)
    weight_kg: Mapped[float | None] = mapped_column(nullable=True)
    height_cm: Mapped[float | None] = mapped_column(nullable=True)
    chest_cm: Mapped[float | None] = mapped_column(nullable=True)
    waist_cm: Mapped[float | None] = mapped_column(nullable=True)
    hips_cm: Mapped[float | None] = mapped_column(nullable=True)
    left_arm_cm: Mapped[float | None] = mapped_column(nullable=True)
    right_arm_cm: Mapped[float | None] = mapped_column(nullable=True)
    left_thigh_cm: Mapped[float | None] = mapped_column(nullable=True)
    right_thigh_cm: Mapped[float | None] = mapped_column(nullable=True)