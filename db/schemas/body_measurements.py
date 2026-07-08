import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class BodyMeasurements(Base):
    __tablename__ = "body_measurements"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    trainer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    gym_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gyms.id"), nullable=False)
    weight_kg: Mapped[float | None] = mapped_column(nullable=True)
    height_cm: Mapped[float | None] = mapped_column(nullable=True)
    chest_cm: Mapped[float | None] = mapped_column(nullable=True)
    waist_cm: Mapped[float | None] = mapped_column(nullable=True)
    hips_cm: Mapped[float | None] = mapped_column(nullable=True)
    left_arm_cm: Mapped[float | None] = mapped_column(nullable=True)
    right_arm_cm: Mapped[float | None] = mapped_column(nullable=True)
    left_thigh_cm: Mapped[float | None] = mapped_column(nullable=True)
    right_thigh_cm: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())